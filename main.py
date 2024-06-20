import logging
import os
from telegram import Update, InputFile
from telegram.constants import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import uuid

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Retrieve bot token and channel ID from environment variables or directly use them
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
CHANNEL_ID = os.getenv('CHANNEL_ID', 'YOUR_CHANNEL_ID_HERE')

# Owners
OWNERS = [6804487024, 930652019]

# Dictionary to store file references with unique IDs
file_store = {}

START_THUMBNAIL_URL = "https://i.ibb.co/FbzmyMj/Whats-App-Image-2024-06-20-at-22-00-27-3fc70e42.jpg"
START_MESSAGE = 'Hi! Send me a file or batch of files and I will store it.'

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message with a thumbnail and start the bot"""
    user_id = update.message.from_user.id
    if user_id in OWNERS:
        # Send the thumbnail image
        context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=START_THUMBNAIL_URL,
            caption=START_MESSAGE,
            parse_mode=ParseMode.HTML
        )
    else:
        update.message.reply_text('You are not authorized to use this bot.')

def handle_document(update: Update, context: CallbackContext) -> None:
    """Handle document uploads from users"""
    user_id = update.message.from_user.id
    if user_id in OWNERS:
        if 'files' not in context.user_data:
            context.user_data['files'] = []
        
        # Get the file from the update and store it in user data
        file = update.message.document
        context.user_data['files'].append(file)
        
        update.message.reply_text('File received! Send more files or use /done to finish uploading.')
    else:
        update.message.reply_text('You are not authorized to use this bot.')

def done(update: Update, context: CallbackContext) -> None:
    """Finalize file upload and generate a unique link"""
    user_id = update.message.from_user.id
    if user_id in OWNERS:
        if 'files' not in context.user_data or not context.user_data['files']:
            update.message.reply_text('No files to store.')
            return
        
        # Generate a unique ID for this batch of files
        unique_id = str(uuid.uuid4())
        file_store[unique_id] = context.user_data['files']
        
        # Send the files to the channel
        for file in context.user_data['files']:
            context.bot.send_document(
                chat_id=CHANNEL_ID, 
                document=file.file_id,
                caption=file.file_name
            )
        
        # Generate a link to share
        link = f'https://t.me/teamflock_file_store_bot?start={unique_id}'
        update.message.reply_text(
            f'Files stored successfully! Share this link to access the files: {link}'
        )
        
        # Clear user data
        context.user_data.clear()
    else:
        update.message.reply_text('You are not authorized to use this bot.')

def handle_start(update: Update, context: CallbackContext) -> None:
    """Handle the /start command with optional parameters"""
    if context.args:
        unique_id = context.args[0]
        if unique_id in file_store:
            files = file_store[unique_id]
            for file in files:
                update.message.reply_document(
                    file.file_id,
                    caption=file.file_name
                )
        else:
            update.message.reply_text('Invalid or expired link.')
    else:
        update.message.reply_text('Hi! Send me a file or batch of files and I will store it.')

def main() -> None:
    """Start the bot"""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states FILE_UPLOAD and FILE_CONFIRMATION
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.document, handle_document)],
        states={
            'FILE_UPLOAD': [MessageHandler(Filters.document, handle_document)],
            'FILE_CONFIRMATION': [CommandHandler('done', done)],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("start", handle_start, pass_args=True))
    
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
    
