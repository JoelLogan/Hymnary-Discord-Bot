"""
Hymnary Discord Bot

A Discord bot that helps users find hymns from hymnary.org using the /find command.
"""

import os
import logging
import discord
from discord import app_commands
from discord.ui import Select, View, Button
from dotenv import load_dotenv
from typing import List, Optional
from sitemap_manager import SitemapManager, initialize_sitemaps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables")

# Initialize Discord client with required intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Global sitemap manager
sitemap_manager: Optional[SitemapManager] = None


class HymnSelectView(View):
    """View with a dropdown menu for selecting a hymn."""
    
    def __init__(self, hymns: List[dict], interaction: discord.Interaction):
        super().__init__(timeout=180)  # 3 minute timeout
        self.hymns = hymns
        self.original_interaction = interaction
        
        # Create select menu
        options = []
        for i, hymn in enumerate(hymns[:25]):  # Discord limit is 25 options
            # Truncate title if too long (100 char limit for option labels)
            title = hymn['title']
            if len(title) > 100:
                title = title[:97] + "..."
            
            options.append(
                discord.SelectOption(
                    label=title,
                    description=hymn['url'][:100] if len(hymn['url']) <= 100 else hymn['url'][:97] + "...",
                    value=str(i)
                )
            )
        
        select = Select(
            placeholder="Choose a hymn to share with the channel...",
            options=options
        )
        select.callback = self.select_callback
        self.add_item(select)
        
        # Add cancel button
        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.secondary)
        cancel_button.callback = self.cancel_callback
        self.add_item(cancel_button)
    
    async def select_callback(self, interaction: discord.Interaction):
        """Handle hymn selection."""
        # Get the selected hymn
        selected_index = int(interaction.data['values'][0])
        selected_hymn = self.hymns[selected_index]
        
        # Send the selected hymn to the channel (non-ephemeral)
        embed = discord.Embed(
            title=selected_hymn['title'],
            url=selected_hymn['url'],
            description=f"🎵 [View on Hymnary]({selected_hymn['url']})",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Shared by {interaction.user.display_name}")
        
        # Send to the channel
        await interaction.response.send_message(embed=embed)
        
        # Update the ephemeral message to confirm
        await self.original_interaction.edit_original_response(
            content=f"✅ Shared: **{selected_hymn['title']}**",
            view=None
        )
        
        self.stop()
    
    async def cancel_callback(self, interaction: discord.Interaction):
        """Handle cancellation."""
        await interaction.response.defer()
        await self.original_interaction.edit_original_response(
            content="❌ Cancelled - no hymn was shared.",
            view=None
        )
        self.stop()


@tree.command(
    name="find",
    description="Search for a hymn on hymnary.org and share it with the channel"
)
@app_commands.describe(
    song_title="The title or partial title of the hymn to search for"
)
async def find_hymn(interaction: discord.Interaction, song_title: str):
    """
    Find a hymn from hymnary.org and allow the user to select which one to share.
    
    Args:
        interaction: The Discord interaction
        song_title: The hymn title to search for
    """
    # Defer the response as searching might take a moment
    await interaction.response.defer(ephemeral=True)
    
    try:
        # Search for hymns
        logger.info(f"Searching for: {song_title}")
        results = sitemap_manager.search_hymns(song_title, max_results=25)
        
        if not results:
            await interaction.followup.send(
                f"❌ No hymns found matching **{song_title}**. Try a different search term.",
                ephemeral=True
            )
            return
        
        # Create embed with search results
        embed = discord.Embed(
            title=f"🔍 Found {len(results)} result{'s' if len(results) != 1 else ''}",
            description=f"Searching for: **{song_title}**\n\nSelect a hymn below to share it with the channel.",
            color=discord.Color.green()
        )
        
        # Create the selection view
        view = HymnSelectView(results, interaction)
        
        await interaction.followup.send(
            embed=embed,
            view=view,
            ephemeral=True
        )
        
    except Exception as e:
        logger.error(f"Error in find_hymn command: {e}", exc_info=True)
        await interaction.followup.send(
            f"❌ An error occurred while searching for hymns: {str(e)}",
            ephemeral=True
        )


@client.event
async def on_ready():
    """Called when the bot is ready."""
    global sitemap_manager
    
    logger.info(f'Logged in as {client.user} (ID: {client.user.id})')
    
    # Initialize sitemap manager
    logger.info("Initializing sitemap manager...")
    sitemap_manager = initialize_sitemaps()
    
    # Load hymn data in the background
    logger.info("Loading hymn data...")
    try:
        hymn_count = len(sitemap_manager.load_all_hymns())
        logger.info(f"Loaded {hymn_count} hymns")
    except Exception as e:
        logger.error(f"Error loading hymns: {e}", exc_info=True)
        logger.warning("Bot will continue but /find may not work properly")
    
    # Sync commands
    try:
        if GUILD_ID:
            # Sync to specific guild for faster testing
            guild = discord.Object(id=int(GUILD_ID))
            tree.copy_global_to(guild=guild)
            await tree.sync(guild=guild)
            logger.info(f"Commands synced to guild {GUILD_ID}")
        else:
            # Global sync (takes up to 1 hour to propagate)
            await tree.sync()
            logger.info("Commands synced globally")
    except Exception as e:
        logger.error(f"Error syncing commands: {e}", exc_info=True)
    
    logger.info("Bot is ready!")


@client.event
async def on_error(event: str, *args, **kwargs):
    """Handle errors."""
    logger.error(f"Error in {event}", exc_info=True)


def main():
    """Run the bot."""
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not set in environment variables")
        return
    
    logger.info("Starting Hymnary Discord Bot...")
    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
