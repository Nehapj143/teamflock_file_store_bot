import logging
import asyncio
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, ConversationHandler
from telegram.ext import filters  # Import filters instead of Filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Replace with your specific bot token and channel ID
BOT_TOKEN = "7167327959:AAFJ25AIsO9olQrSzV2OcM0YqY7yUzWekDQ"
CHANNEL_ID = "-1001329275814"

# Owners
OWNERS = [6804487024, 930652019]

# Dictionary to store file references with unique IDs
file_store = {}

# URL for Render web service
RENDER_URL = "https://teamflock-file-store-bot.onrender.com"

# Constants for conversation states
FILE_UPLOAD, FILE_CONFIRMATION = range(2)

# Thumbnail and start message
START_THUMBNAIL_URL = "https://i.ibb.co/FbzmyMj/Whats-App-Image-2024-06-20-at-22-00-27-3fc70e42.jpg"
START_MESSAGE = 'Hi! Send me a file or batch of files and I will store it.'

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message with a thumbnail and start the bot"""
    user_id = update.message.from_user.id
    if user_id in OWNERS:
        # Send the thumbnail image
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=START_THUMBNAIL_URL,
            caption=START_MESSAGE,
            parse_mode=ParseMode.HTML  # Using ParseMode.HTML for HTML formatting
        )
    else:
        await update.message.reply_text('You are not authorized to use this bot.')

async def handle_document(update: Update, context: CallbackContext) -> int:
    """Handle document uploads from users"""
    user_id = update.message.from_user.id
    if user_id in OWNERS:
        if 'files' not in context.user_data:
            context.user_data['files'] = []
        
        # Get the file from the update and store it in user data
        file = update.message.document
        context.user_data['files'].append(file)
        
        await update.message.reply_text('File received! Send more files or use /done to finish uploading.')
        return FILE_UPLOAD
    else:
        await update.message.reply_text('You are not authorized to use this bot.')

async def done(update: Update, context: CallbackContext) -> None:
    """Finalize file upload and generate a unique link"""
    user_id = update.message.from_user.id
    if user_id in OWNERS:
        if 'files' not in context.user_data or not context.user_data['files']:
            await update.message.reply_text('No files to store.')
            return
        
        # Generate a unique ID for this batch of files
        unique_id = str(uuid.uuid4())
        file_store[unique_id] = context.user_data['files']
        
        # Send the files to the channel
        for file in context.user_data['files']:
            await context.bot.send_document(
                chat_id=CHANNEL_ID, 
                document=file.file_id,
                caption=file.file_name
            )
        
        # Generate links to share
        bot_link = f'https://t.me/{context.bot.username}?start={unique_id}'
        render_link = f'{RENDER_URL}/{unique_id}'
        
        await update.message.reply_text(
            f'Files stored successfully! Share these links to access the files:\n'
            f'Telegram Bot: {bot_link}\n'
            f'Render: {render_link}'
        )
        
        # Clear user data
        context.user_data.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text('You are not authorized to use this bot.')

async def handle_start(update: Update, context: CallbackContext) -> None:
    """Handle the /start command with optional parameters"""
    if context.args:
        unique_id = context.args[0]
        if unique_id in file_store:
            files = file_store[unique_id]
            for file in files:
                await update.message.reply_document(
                    file.file_id,
                    caption=file.file_name
                )
        else:
            await update.message.reply_text('Invalid or expired link.')
    else:
        await update.message.reply_text('Hi! Send me a file or batch of files and I will store it.')

async def main() -> None:
    """Start the bot"""
    bot = Bot(token=BOT_TOKEN)
    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.DocumentFilter(), handle_document)],  # Using filters.DocumentFilter()
        states={
            FILE_UPLOAD: [MessageHandler(filters.DocumentFilter(), handle_document)],
            FILE_CONFIRMATION: [CommandHandler('done', done)],
        },
        fallbacks=[CommandHandler('start', handle_start, pass_args=True)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("start", handle_start, pass_args=True))

    await updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    asyncio.run(main())

