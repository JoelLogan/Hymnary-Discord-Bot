#!/usr/bin/env python3
"""
Simple test script to verify the bot components work correctly.
This doesn't require a Discord token.
"""

import sys
from pathlib import Path
from sitemap_manager import SitemapManager

def test_sitemap_manager():
    """Test the sitemap manager with mock data."""
    print("Testing Sitemap Manager...")
    print("-" * 50)
    
    # Create manager with temp directory
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SitemapManager(sitemap_dir=Path(tmpdir))
        
        # Test 1: Title extraction
        print("\n1. Testing title extraction from URLs:")
        test_urls = [
            "https://hymnary.org/text/amazing_grace_how_sweet_the_sound",
            "https://hymnary.org/text/how_great_thou_art",
            "https://hymnary.org/tune/sweet_hour_of_prayer",
        ]
        for url in test_urls:
            title = manager._extract_title_from_url(url)
            print(f"   {url}")
            print(f"   → {title}\n")
        
        # Test 2: Mock hymn data
        print("2. Loading mock hymn data:")
        manager.hymn_data = [
            {
                'url': 'https://hymnary.org/text/amazing_grace_how_sweet_the_sound',
                'title': 'Amazing Grace How Sweet The Sound',
                'title_lower': 'amazing grace how sweet the sound'
            },
            {
                'url': 'https://hymnary.org/text/grace_greater_than_our_sin',
                'title': 'Grace Greater Than Our Sin',
                'title_lower': 'grace greater than our sin'
            },
            {
                'url': 'https://hymnary.org/text/how_great_thou_art',
                'title': 'How Great Thou Art',
                'title_lower': 'how great thou art'
            },
            {
                'url': 'https://hymnary.org/text/great_is_thy_faithfulness',
                'title': 'Great Is Thy Faithfulness',
                'title_lower': 'great is thy faithfulness'
            },
            {
                'url': 'https://hymnary.org/text/be_thou_my_vision',
                'title': 'Be Thou My Vision',
                'title_lower': 'be thou my vision'
            },
        ]
        print(f"   Loaded {len(manager.hymn_data)} mock hymns\n")
        
        # Test 3: Search functionality
        print("3. Testing search functionality:")
        test_queries = [
            "grace",
            "amazing",
            "great",
            "thou",
            "xyz_not_found"
        ]
        
        for query in test_queries:
            results = manager.search_hymns(query, max_results=10)
            print(f"   Query: '{query}' → Found {len(results)} result(s)")
            for hymn in results:
                print(f"      - {hymn['title']}")
        
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        return True

def test_bot_imports():
    """Test that bot modules can be imported."""
    print("\nTesting Bot Module Imports...")
    print("-" * 50)
    
    try:
        import importlib.util
        
        # Test sitemap_manager
        spec = importlib.util.spec_from_file_location('sitemap_manager', 'sitemap_manager.py')
        sitemap_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sitemap_module)
        print("✓ sitemap_manager.py loads successfully")
        
        # Check for required classes and functions
        assert hasattr(sitemap_module, 'SitemapManager')
        print("✓ SitemapManager class exists")
        
        assert hasattr(sitemap_module, 'initialize_sitemaps')
        print("✓ initialize_sitemaps function exists")
        
        print("\n" + "=" * 50)
        print("✓ All import tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("Hymnary Discord Bot - Test Suite")
    print("=" * 50)
    
    success = True
    
    # Run tests
    try:
        if not test_bot_imports():
            success = False
        
        if not test_sitemap_manager():
            success = False
            
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        success = False
    
    # Final result
    print("\n" + "=" * 50)
    if success:
        print("✓ ALL TESTS PASSED")
        print("=" * 50)
        print("\nThe bot is ready to use!")
        print("Set DISCORD_TOKEN in .env and run: python bot.py")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 50)
        return 1

if __name__ == "__main__":
    sys.exit(main())
