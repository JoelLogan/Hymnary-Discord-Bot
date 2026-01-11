"""
Hymnary Sitemap Downloader and Parser

This module handles downloading, extracting, and parsing sitemap files from hymnary.org.
"""

import os
import re
import gzip
import shutil
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional
import requests

logger = logging.getLogger(__name__)

SITEMAP_DIR = Path("sitemaps")
SITEMAP_INDEX_URL = "https://hymnary.org/sitemap.xml"


class SitemapManager:
    """Manages downloading and parsing of Hymnary sitemaps."""
    
    def __init__(self, sitemap_dir: Path = SITEMAP_DIR):
        self.sitemap_dir = sitemap_dir
        self.sitemap_dir.mkdir(exist_ok=True)
        self.sitemap_urls: List[str] = []
        self.hymn_data: List[Dict[str, str]] = []
        
    def download_file(self, url: str, destination: Path) -> bool:
        """Download a file from URL to destination."""
        try:
            logger.info(f"Downloading {url}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(destination, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Downloaded to {destination}")
            return True
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            return False
    
    def extract_gz_file(self, gz_path: Path) -> Optional[Path]:
        """Extract a .gz file and return the path to the extracted file."""
        try:
            output_path = gz_path.with_suffix('')
            
            with gzip.open(gz_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            logger.info(f"Extracted {gz_path} to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error extracting {gz_path}: {e}")
            return None
    
    def parse_sitemap_index(self) -> List[str]:
        """Parse the main sitemap index to get URLs of individual sitemaps."""
        index_path = self.sitemap_dir / "sitemap.xml"
        
        # Download if not exists
        if not index_path.exists():
            if not self.download_file(SITEMAP_INDEX_URL, index_path):
                logger.error("Failed to download sitemap index")
                return []
        
        try:
            tree = ET.parse(index_path)
            root = tree.getroot()
            
            # Handle XML namespace
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            urls = []
            for sitemap in root.findall('.//ns:sitemap', namespace):
                loc = sitemap.find('ns:loc', namespace)
                if loc is not None and loc.text:
                    urls.append(loc.text)
            
            self.sitemap_urls = urls
            logger.info(f"Found {len(urls)} sitemap URLs")
            return urls
        except Exception as e:
            logger.error(f"Error parsing sitemap index: {e}")
            return []
    
    def download_and_extract_sitemaps(self, limit: Optional[int] = None) -> List[Path]:
        """Download and extract individual sitemap files."""
        if not self.sitemap_urls:
            self.parse_sitemap_index()
        
        extracted_files = []
        urls_to_process = self.sitemap_urls[:limit] if limit else self.sitemap_urls
        
        for url in urls_to_process:
            filename = url.split('/')[-1]
            gz_path = self.sitemap_dir / filename
            
            # Check if already extracted
            xml_path = gz_path.with_suffix('')
            if xml_path.exists():
                logger.info(f"Already exists: {xml_path}")
                extracted_files.append(xml_path)
                continue
            
            # Download if needed
            if not gz_path.exists():
                if not self.download_file(url, gz_path):
                    continue
            
            # Extract
            xml_path = self.extract_gz_file(gz_path)
            if xml_path:
                extracted_files.append(xml_path)
        
        return extracted_files
    
    def parse_sitemap_file(self, xml_path: Path) -> List[Dict[str, str]]:
        """Parse a sitemap XML file and extract hymn information."""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            hymns = []
            for url_element in root.findall('.//ns:url', namespace):
                loc = url_element.find('ns:loc', namespace)
                if loc is not None and loc.text:
                    url = loc.text
                    
                    # Extract title from URL
                    # URLs like: https://hymnary.org/text/amazing_grace_how_sweet_the_sound
                    title = self._extract_title_from_url(url)
                    
                    hymns.append({
                        'url': url,
                        'title': title,
                        'title_lower': title.lower()
                    })
            
            return hymns
        except Exception as e:
            logger.error(f"Error parsing {xml_path}: {e}")
            return []
    
    def _extract_title_from_url(self, url: str) -> str:
        """Extract readable title from URL."""
        # Get the last part of the URL
        parts = url.rstrip('/').split('/')
        if len(parts) > 0:
            slug = parts[-1]
            # Replace underscores with spaces and capitalize
            title = slug.replace('_', ' ').title()
            return title
        return url
    
    def load_all_hymns(self, force_reload: bool = False) -> List[Dict[str, str]]:
        """Load all hymn data from sitemaps."""
        if self.hymn_data and not force_reload:
            return self.hymn_data
        
        # Download and extract sitemaps (limit to text sitemaps for hymns)
        logger.info("Loading sitemaps...")
        extracted_files = self.download_and_extract_sitemaps()
        
        all_hymns = []
        for xml_file in extracted_files:
            # Focus on text sitemaps which contain hymn texts
            if 'text' in xml_file.name.lower():
                hymns = self.parse_sitemap_file(xml_file)
                all_hymns.extend(hymns)
                logger.info(f"Loaded {len(hymns)} hymns from {xml_file.name}")
        
        self.hymn_data = all_hymns
        logger.info(f"Total hymns loaded: {len(all_hymns)}")
        return all_hymns
    
    def search_hymns(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Search for hymns matching the query using regex."""
        if not self.hymn_data:
            self.load_all_hymns()
        
        try:
            # Create a regex pattern that's flexible with the query
            # Replace spaces with optional underscores/spaces
            pattern = query.lower().strip()
            pattern = re.escape(pattern)
            pattern = pattern.replace(r'\ ', r'[\s_]+')
            
            regex = re.compile(pattern, re.IGNORECASE)
            
            matches = []
            for hymn in self.hymn_data:
                if regex.search(hymn['title_lower']):
                    matches.append(hymn)
                    if len(matches) >= max_results:
                        break
            
            return matches
        except Exception as e:
            logger.error(f"Error searching hymns: {e}")
            return []


def initialize_sitemaps():
    """Initialize and download sitemaps on bot startup."""
    manager = SitemapManager()
    try:
        # Download just a few sitemaps initially to be quick
        # Full download can happen in background or on-demand
        manager.parse_sitemap_index()
        logger.info("Sitemap initialization complete")
        return manager
    except Exception as e:
        logger.error(f"Error initializing sitemaps: {e}")
        return manager
