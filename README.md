# Hymnary Discord Bot

A Discord bot that helps users find and share hymns from [hymnary.org](https://hymnary.org) using an intuitive slash command interface.

## Features

- 🔍 **Search hymns** using the `/find` command with flexible regex matching
- 📋 **Private selection** - Search results appear only to you
- 🎵 **Share with channel** - Select a hymn to share with everyone
- 📥 **Auto-download sitemaps** - Automatically downloads and parses hymnary.org sitemaps
- ⚡ **Fast searching** - Searches through local sitemap cache for quick results

## Setup

### Prerequisites

- Python 3.8 or higher
- A Discord Bot Token from the [Discord Developer Portal](https://discord.com/developers/applications)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JoelLogan/Hymnary-Discord-Bot.git
   cd Hymnary-Discord-Bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```
   
   Optional: Add a guild ID for faster command sync during testing:
   ```
   GUILD_ID=your_guild_id_here
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

   On first run, the bot will download and extract sitemap files from hymnary.org. This may take a few minutes depending on your internet connection.

## Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token and add it to your `.env` file
5. Enable the following **Privileged Gateway Intents**:
   - Message Content Intent (if you plan to add message-based features later)
6. Go to "OAuth2" → "URL Generator"
7. Select scopes: `bot` and `applications.commands`
8. Select bot permissions: 
   - Send Messages
   - Embed Links
   - Read Message History
9. Use the generated URL to invite the bot to your server

## Usage

### `/find` Command

Search for a hymn and share it with your channel.

**Syntax:**
```
/find song_title: <hymn title or keywords>
```

**Example:**
```
/find song_title: Amazing Grace
```

**How it works:**
1. Type `/find` and enter the hymn title or keywords
2. The bot searches through hymnary.org sitemaps using regex matching
3. Results appear in a **private message** (only you can see it)
4. Select the correct hymn from the dropdown menu
5. The selected hymn is **shared with the entire channel**
6. Or click "Cancel" to dismiss without sharing

## Project Structure

```
Hymnary-Discord-Bot/
├── bot.py                 # Main bot file with Discord commands
├── sitemap_manager.py     # Sitemap downloading and searching logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── sitemaps/             # Downloaded sitemap files (auto-generated)
```

## Technical Details

### Sitemap Management

- Downloads sitemap index from `https://hymnary.org/sitemap.xml`
- Extracts individual `.xml.gz` sitemap files
- Focuses on `text` sitemaps which contain hymn information
- Caches sitemaps locally for faster subsequent searches

### Search Algorithm

- Uses Python regex for flexible pattern matching
- Searches hymn titles extracted from sitemap URLs
- Case-insensitive matching
- Handles spaces and underscores interchangeably
- Returns up to 25 results (Discord select menu limit)

### Discord Integration

- Uses discord.py with slash commands (app_commands)
- Ephemeral messages for private search results
- Select menus for hymn selection
- Embeds for rich formatting
- Button for canceling selection

## Development

### Running in Development

For faster command sync during development, set the `GUILD_ID` in your `.env` file:

```
GUILD_ID=your_test_server_id
```

This syncs commands instantly to your test server instead of waiting for global sync (which can take up to 1 hour).

### Logging

The bot uses Python's logging module. Logs include:
- Bot startup and initialization
- Sitemap downloads and parsing
- Command executions
- Errors and exceptions

## Troubleshooting

**Bot doesn't respond to `/find` command:**
- Make sure the bot has been invited with the `applications.commands` scope
- Wait a few minutes for command sync (or use GUILD_ID for instant sync)
- Check bot permissions in the channel

**No hymns found:**
- Verify sitemaps downloaded correctly (check `sitemaps/` directory)
- Try different search terms or partial titles
- Check logs for errors

**Sitemaps not downloading:**
- Check internet connection
- Verify hymnary.org is accessible
- Check logs for specific error messages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Hymn data provided by [hymnary.org](https://hymnary.org)
- Built with [discord.py](https://github.com/Rapptz/discord.py)