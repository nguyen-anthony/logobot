# Discord Server Logo Cycler

A simple Python script that automatically cycles through server logos/icons for your Discord server.

## Prerequisites

### For Docker Usage
1. Install Docker Desktop for Windows from [Docker's official website](https://www.docker.com/products/docker-desktop)
2. Start Docker Desktop before running any Docker commands
3. Make sure Docker Desktop is running (you should see the Docker icon in your system tray)

## Setup

1. Create a Discord bot and get its token:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a New Application
   - Go to the "Bot" section and create a bot
   - Copy the bot token

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `logos` directory and add your images:
   - Create a directory named `logos` in the same folder as the script
   - Add your PNG or JPG images to this directory
   - Make sure images are square and under 8MB (Discord's requirements)

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your bot token
   - Add your server (guild) ID
   - Optionally adjust the cycle interval (in seconds)

5. Invite the bot to your server:
   - Go to OAuth2 > URL Generator in the Developer Portal
   - Select "bot" scope
   - Select "Manage Server" permission
   - Use the generated URL to invite the bot

## Usage

### Running Locally

Simply run the script:
```bash
python logo_cycler.py
```

### Running with Docker

You can run the bot using either Docker directly or Docker Compose.

#### Using Docker Compose (Recommended)

1. Make sure Docker Desktop is running
2. Start the bot:
   ```bash
   docker compose up -d
   ```

3. View logs:
   ```bash
   docker compose logs -f
   ```

4. Stop the bot:
   ```bash
   docker compose down
   ```

#### Using Docker Directly

1. Make sure Docker Desktop is running
2. Build the Docker image:
   ```bash
   docker build -t discord-logo-cycler .
   ```

3. Run the container:
   ```bash
   docker run -d \
     --name discord-logo-cycler \
     -v $(pwd)/logos:/app/logos \
     --env-file .env \
     discord-logo-cycler
   ```

   Note: Replace `$(pwd)` with the full path to your project directory on Windows.

4. View logs:
   ```bash
   docker logs discord-logo-cycler
   ```

5. Stop the container:
   ```bash
   docker stop discord-logo-cycler
   ```

The script will:
- Connect to Discord
- Randomly select an image from the `logos` directory
- Change the server icon
- Wait for the specified interval
- Repeat the process

## Notes

- The default cycle interval is 1 hour (3600 seconds)
- The script will randomly select from all PNG and JPG files in the `logos` directory
- Make sure your bot has the "Manage Server" permission
- Server icons must be square images
- Maximum file size for server icons is 8MB
- When using Docker, the `logos` directory is mounted as a volume, so you can update the images without rebuilding the container
- The Docker Compose setup includes automatic restart and log rotation 