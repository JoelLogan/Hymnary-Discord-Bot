# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Discord Platform                        │
│  ┌─────────────┐         ┌──────────────┐                  │
│  │   User A    │         │    User B    │                  │
│  │ Types: /find│         │  Sees result │                  │
│  └──────┬──────┘         └──────▲───────┘                  │
│         │                       │                           │
└─────────┼───────────────────────┼───────────────────────────┘
          │                       │
          │ 1. Slash Command      │ 5. Public Message
          │                       │
┌─────────▼───────────────────────┴───────────────────────────┐
│                  Hymnary Discord Bot                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  bot.py (Main Discord Bot)                           │  │
│  │  - Handles /find command                             │  │
│  │  - Creates ephemeral UI (dropdown + cancel button)   │  │
│  │  - Processes user selection                          │  │
│  │  - Posts result to channel                           │  │
│  └─────────────┬────────────────────────────────────────┘  │
│                │                                            │
│                │ 2. Search Query                            │
│                │ 4. Search Results                          │
│                ▼                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  sitemap_manager.py (Search Engine)                  │  │
│  │  - Downloads sitemaps on startup                     │  │
│  │  - Extracts and parses XML files                     │  │
│  │  - Maintains hymn database in memory                 │  │
│  │  - Performs regex-based search                       │  │
│  └─────────────┬────────────────────────────────────────┘  │
│                │                                            │
└────────────────┼────────────────────────────────────────────┘
                 │
                 │ 3. Download & Parse
                 │ (First run only)
                 ▼
┌──────────────────────────────────────────────────────────────┐
│                     Hymnary.org                              │
│  - sitemap.xml (index)                                       │
│  - index_text_0.xml.gz, index_text_1.xml.gz, etc.           │
│  - Contains URLs and metadata for all hymns                  │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

### Command Execution Flow

1. **User Initiates Search**
   - User types: `/find song_title: Amazing Grace`
   - Discord sends command to bot

2. **Bot Processes Query**
   - Bot receives slash command
   - Defers response (ephemeral)
   - Calls sitemap_manager.search_hymns()

3. **Search Execution**
   - Sitemap manager searches local database
   - Uses regex pattern matching
   - Returns up to 25 matching hymns

4. **Results Display** (Ephemeral - Private)
   - Bot creates Discord Select menu with results
   - Adds Cancel button
   - Sends ephemeral message to user
   - Only the user who ran the command sees this

5. **User Selection**
   - User selects hymn from dropdown OR clicks Cancel
   - Selection triggers callback

6. **Result Sharing** (Public)
   - Bot creates rich embed with hymn info
   - Posts to channel (everyone can see)
   - Updates ephemeral message with confirmation
   - Or shows cancellation message

## Component Details

### bot.py
- **Purpose**: Discord interaction layer
- **Key Functions**:
  - `find_hymn()`: Handles /find command
  - `HymnSelectView`: UI for hymn selection
  - `on_ready()`: Bot initialization

### sitemap_manager.py
- **Purpose**: Data management and search
- **Key Classes**:
  - `SitemapManager`: Main class for sitemap operations
- **Key Functions**:
  - `download_and_extract_sitemaps()`: Gets sitemap data
  - `parse_sitemap_file()`: Extracts hymn info
  - `search_hymns()`: Regex-based search
  - `load_all_hymns()`: Loads data into memory

## Storage

### Local File System
```
sitemaps/
├── sitemap.xml                    # Main index
├── index_text_0.xml               # Extracted sitemap
├── index_text_0.xml.gz           # Downloaded file
├── index_text_1.xml
├── index_text_1.xml.gz
└── ...
```

### In-Memory Database
- Hymn data stored as Python list of dictionaries
- Structure:
  ```python
  {
    'url': 'https://hymnary.org/text/amazing_grace',
    'title': 'Amazing Grace',
    'title_lower': 'amazing grace'  # For search
  }
  ```

## Security Features

1. **Environment Variables**: Token stored in .env file
2. **Dependency Security**: All dependencies scanned for vulnerabilities
3. **Input Validation**: User input sanitized through Discord
4. **Ephemeral Messages**: Search history not visible to others
5. **Thread-Safe**: Async lock prevents race conditions

## Performance Considerations

1. **Startup Time**: 
   - Initial sitemap download: 30-60 seconds (first run)
   - Subsequent starts: <5 seconds (uses cache)

2. **Search Time**:
   - In-memory search: <100ms for most queries
   - Regex compilation cached

3. **Memory Usage**:
   - ~50-100MB for sitemap data
   - Scales with number of hymns in database

## Scalability

- **Current**: Single-server bot
- **Sitemaps**: Downloaded once, cached locally
- **Concurrent Users**: Discord.py handles async requests
- **Search**: In-memory, fast for moderate databases

## Future Enhancements

Possible improvements:
1. Database storage (SQLite/PostgreSQL)
2. Caching recent searches
3. Fuzzy matching for typos
4. Additional search filters
5. Support for tunes, authors, meters
6. Periodic sitemap updates
