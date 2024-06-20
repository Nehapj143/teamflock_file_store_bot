# teamflock_file_store_bot
Here's a `README.md` file for your GitHub repository:

```markdown
# TeamFlock File Store Bot

A Telegram bot that allows authorized users to upload files to a private channel and generate unique links for others to access those files. 

## Features

- Upload single or multiple files.
- Store files in a private Telegram channel.
- Generate unique links for accessing stored files.
- Only authorized users can upload and share files.
- Sends a welcome message with a thumbnail image.

## Prerequisites

- Python 3.6+
- Telegram Bot API token
- Private Telegram channel ID

## Getting Started

### Clone the Repository

```sh
git clone https://github.com/yourusername/teamflock_file_store_bot.git
cd teamflock_file_store_bot
```

### Setting Up Environment Variables

Create a `.env` file in the root directory and add your bot token and channel ID:

```env
BOT_TOKEN=your_bot_token_here
CHANNEL_ID=your_channel_id_here
```

Alternatively, you can directly modify the `main.py` file to include your bot token and channel ID:

```python
BOT_TOKEN = 'your_bot_token_here'
CHANNEL_ID = 'your_channel_id_here'
```

### Install Dependencies

Install the required Python packages using pip:

```sh
pip install -r requirements.txt
```

### Running the Bot Locally

Run the bot using the following command:

```sh
./start.sh
```

### Deploying on Render

1. **Create an Account on Render:**
   - Sign up at [Render](https://render.com/).

2. **Create a New Web Service:**
   - Go to your Render dashboard.
   - Click on the "New" button and select "Web Service."
   - Connect your GitHub account and select the repository `teamflock_file_store_bot`.

3. **Configure the Service:**
   - **Environment:** Select `Python 3`.
   - **Build Command:** Leave it blank (Render automatically installs dependencies from `requirements.txt`).
   - **Start Command:** `./start.sh`.

4. **Set Environment Variables:**
   - After the service is created, go to the "Environment" tab.
   - Add the environment variables `BOT_TOKEN` and `CHANNEL_ID`.

5. **Deploy the Service:**
   - Render will automatically start the deployment process.
   - Once the deployment is complete, your bot will be up and running.

## Usage

1. **Start the Bot:**
   - Open Telegram and start a chat with your bot using the username provided during bot creation.

2. **Upload Files:**
   - Authorized users can send files directly to the bot. 
   - After uploading files, use the `/done` command to finalize and get a shareable link.

3. **Access Files:**
   - Share the generated link with others to allow them to access the files via the bot.

## Owners

To restrict file uploads to specific users, update the `OWNERS` list in `main.py` with the Telegram user IDs of the authorized users:

```python
OWNERS = [6804487024, 930652019]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgments

- [Python Telegram Bot](https://python-telegram-bot.org/)
- [Render](https://render.com/)
```

### Final Steps

1. **Update Repository URL:**
   Replace `https://github.com/yourusername/teamflock_file_store_bot.git` with the actual URL of your GitHub repository.

2. **Add License:**
   Add a `LICENSE` file if you wish to include a license for your project.

3. **Customize as Needed:**
   Modify any sections as needed to better fit your specific use case or additional setup instructions.

Once you've completed these steps, you can commit the `README.md` file to your repository. This will help other developers and users understand how to use and contribute to your project.
