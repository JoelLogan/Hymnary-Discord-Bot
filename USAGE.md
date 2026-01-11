# Usage Examples

This document provides detailed examples of using the Hymnary Discord Bot.

## Basic Usage

### Searching for a Hymn

The simplest way to use the bot is with the `/find` command:

```
/find song_title: Amazing Grace
```

When you execute this command:
1. A private message appears with search results (only you can see it)
2. The results show hymns matching your search
3. Select the hymn you want from the dropdown menu
4. The selected hymn is shared with the entire channel
5. Everyone can see the hymn you selected

### Search Tips

**Partial titles work great:**
```
/find song_title: grace
```
This will find:
- Amazing Grace
- Grace Greater Than Our Sin
- Grace Alone
- And any other hymn with "grace" in the title

**Multiple words:**
```
/find song_title: how great thou art
```
The search uses regex, so it's flexible with spacing and capitalization.

**Specific phrases:**
```
/find song_title: sweet hour of prayer
```

## Example Scenarios

### Scenario 1: Leading Worship Planning

You're planning worship and want to share a hymn with your team:

1. Type: `/find song_title: be thou my vision`
2. See the results privately (your team doesn't see the search)
3. Select "Be Thou My Vision" from the dropdown
4. The hymn is shared in the channel with a link to hymnary.org
5. Your team can click the link to see the full hymn

### Scenario 2: Finding a Hymn You Don't Remember Completely

You remember part of a hymn title:

1. Type: `/find song_title: great`
2. Browse through results:
   - How Great Thou Art
   - Great Is Thy Faithfulness
   - Grace Greater Than Our Sin
3. Select the one you were thinking of
4. Share it with the channel

### Scenario 3: Canceling a Search

If you change your mind:

1. Type: `/find song_title: amazing grace`
2. See the results privately
3. Click the "Cancel" button
4. Nothing is shared with the channel

## Understanding the Results

### Private Search Results

When you use `/find`, you get a private message that looks like:

```
🔍 Found 3 results
Searching for: amazing grace

Select a hymn below to share it with the channel.

[Dropdown menu with options]
[Cancel button]
```

Only you can see this message. It disappears after 3 minutes of inactivity.

### Shared Result

When you select a hymn, everyone in the channel sees:

```
🎵 Amazing Grace How Sweet The Sound

View on Hymnary
(link to https://hymnary.org/text/amazing_grace_how_sweet_the_sound)

Shared by YourUsername
```

## Advanced Usage

### Search Techniques

The bot uses regex for searching, which means:

- **Case insensitive**: "grace" = "Grace" = "GRACE"
- **Flexible spacing**: "amazing grace" matches URLs like `amazing_grace`
- **Partial matches**: "great" finds "Great Is Thy Faithfulness"

### Multiple Results

The bot returns up to 25 results (Discord's limit for select menus). If your search term is too broad:

```
/find song_title: the
```

You'll get the first 25 hymns with "the" in the title. Try to be more specific if possible.

## Troubleshooting

### "No hymns found"

If you get this message:
- Check your spelling
- Try a shorter search term
- Try just one word from the title
- Example: Instead of "sweet hour of prayer in the morning", try "sweet hour"

### Command Not Appearing

If you don't see the `/find` command:
- Make sure the bot has been added to your server
- Wait a few minutes after the bot was added (commands need to sync)
- Check that the bot has proper permissions

### Search Takes a Long Time

The first search after bot restart may take longer because:
- The bot is downloading sitemap files
- This only happens once per bot restart
- Subsequent searches are fast

## Best Practices

1. **Be specific when possible**: "Amazing Grace" is better than just "grace"
2. **Use the cancel button**: If you searched for the wrong thing, cancel instead of selecting a random result
3. **Check the URL**: The dropdown shows the hymnary.org URL so you can verify it's the right hymn
4. **One word searches**: Great for browsing (e.g., `/find song_title: joy` to see all hymns about joy)

## Support

If you encounter issues:
1. Check the bot's status (is it online?)
2. Try a simpler search term
3. Make sure you have permission to use commands in the channel
4. Contact the bot administrator if problems persist
