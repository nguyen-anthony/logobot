import discord
import os
import asyncio
from dotenv import load_dotenv
from pathlib import Path
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

MIN_INTERVAL = 3 * 60 * 60  # 3 hours
MAX_INTERVAL = 8 * 60 * 60  # 8 hours

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_available_logos(logo_dir: Path, last_used_logo: Path | None) -> list[Path]:
    """Get list of available logos, excluding the last used one."""
    # Use case-insensitive glob for better cross-platform compatibility
    logo_files = []
    for ext in ['*.png', '*.jpg', '*.PNG', '*.JPG']:
        logo_files.extend(list(logo_dir.glob(ext)))
    
    if not logo_files:
        print("No logo files found in the logos directory!")
        return []
    
    # Filter out the last used logo if it exists
    available_logos = [logo for logo in logo_files if logo != last_used_logo]
    
    # If we only have one logo, we'll have to use it
    if not available_logos:
        available_logos = logo_files
    
    return available_logos

def get_random_interval() -> int:
    """Get a random interval between MIN_INTERVAL and MAX_INTERVAL."""
    interval = random.randint(MIN_INTERVAL, MAX_INTERVAL)
    hours = interval / 3600
    print(f"Next logo change will occur in {hours:.1f} hours")
    return interval

async def update_server_icon(guild: discord.Guild, logo_path: Path) -> None:
    """Update the server icon with the given logo."""
    try:
        with open(logo_path, 'rb') as image:
            icon_bytes = image.read()
        await guild.edit(icon=icon_bytes)
        print(f"Updated server icon to: {logo_path.name}")
    except discord.HTTPException as e:
        print(f"Discord API error while updating icon: {e}")
        raise
    except Exception as e:
        print(f"Error reading or updating icon: {e}")
        raise

async def cycle_logo():
    await client.wait_until_ready()
    
    # Keep track of the last used logo
    last_used_logo = None
    
    while not client.is_closed():
        try:
            guild = client.get_guild(GUILD_ID)
            if not guild:
                print(f"Could not find guild with ID {GUILD_ID}")
                return

            # Get available logos
            logo_dir = Path('logos').resolve()  # Resolve to absolute path
            if not logo_dir.exists():
                print(f"Logos directory not found at: {logo_dir}")
                return
                
            available_logos = get_available_logos(logo_dir, last_used_logo)
            if not available_logos:
                return

            # Select and update logo
            logo_path = random.choice(available_logos)
            last_used_logo = logo_path
            await update_server_icon(guild, logo_path)

            # Wait for random interval
            next_interval = get_random_interval()
            await asyncio.sleep(next_interval)

        except Exception as e:
            print(f"Error occurred while changing logo: {e}")
            # If there's an error, wait for a minimum interval before retrying
            await asyncio.sleep(MIN_INTERVAL)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(cycle_logo())

client.run(TOKEN) 