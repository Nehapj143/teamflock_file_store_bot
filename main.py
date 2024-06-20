import logging
import re
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ConversationHandler
import uuid
import time
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='user_data.log', filemode='a')

TOKEN = '7167327959:AAFJ25AIsO9olQrSzV2OcM0YqY7yUzWekDQ'
CHANNEL_ID = '-1001329275814'
LOG_CHANNEL_ID = '-1002035396400'
GOFIL.IO_ACCOUNT_ID = 'f6f34dc8-c55c-4d4c-b272-0aaad3820dd9'
GOFIL.IO_API_KEY = 'xdqmdwlfDftnNGxVuDlA2WZncahb14Dv'

FILE_UPLOAD, FILE_CONFIRM, LINK_SHARE = range(3)

def start(update, context):
    update.message.reply_text('Welcome! Please upload a file.')
    return FILE_UPLOAD

def handle_document(update, context):
    file = update.message.document
    file_id = file.file_id
    file_unique_id = str(uuid.uuid4())
    context.user_data['file_id'] = file_id
    context.user_data['file_unique_id'] = file_unique_id
    update.message.reply_text('File uploaded successfully! Please confirm to generate a link.')
    return FILE_CONFIRM

def done(update, context):
    file_id = context.user_data['file_id']
    file_unique_id = context.user_data['file_unique_id']
    caption = update.message.caption
    if caption:
        # Remove unwanted text from caption
        unwanted_text = r'(RipcrabbyAnime|www\.1TamilMV\.eu|BollyFlix|UHDMovies|vegamovies|\[Toonworld4all\]|http://thepwc\.xyz|mkvCinemas|mkvAnime|@WrestlingMultiverse|@Wrestling_Asylum|@ClipmateMovies|@Ongoing_Fair|@infinite_anime|privatemoviez|OlAM|PSA|Pahe)'
        caption = re.sub(unwanted_text, '', caption, flags=re.IGNORECASE)
        context.bot.send_document(chat_id=CHANNEL_ID, document=file_id, caption=caption)
    else:
        context.bot.send_document(chat_id=CHANNEL_ID, document=file_id)
    
    # Upload file to gofile.io
    file_info = context.bot.get_file(file_id)
    file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
    response = requests.get(file_url, stream=True)
    file_name = file_info.file_name
    gofile_response = requests.post('https://api.gofile.io/uploadFile', files={'file': (file_name, response.raw)}, data={'token': GOFIL.IO_API_KEY, 'account_id': GOFIL.IO_ACCOUNT_ID})
    gofile_link = gofile_response.json()['data']['link']
    
    update.message.reply_text(f'File link: https://example.com/{file_unique_id}')
    update.message.reply_text(f'Gofile link: {gofile_link}')
    update.message.reply_text('Warning: Your conversation data will be deleted in 30 minutes. Please forward the file to another location to keep it permanently.')
    
    # Log user data to the log channel
    log_message = f'User {update.effective_user.username} uploaded a file with ID {file_unique_id}'
    logging.info(log_message)
    context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_message)
    
    return ConversationHandler.END

def handle_start(update, context):
    args = update.message.text.split()
    if len(args) > 1:
        file_unique_id = args[1]
        # Retrieve file from the channel based on unique ID and send it back to the user
        context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=CHANNEL_ID, message_id=file_unique_id)
    else:
        update.message.reply_text('Invalid command. Please use /start <file_unique_id> to retrieve a file.')
    return ConversationHandler.END

def delete_conversation_data(context):
    # Delete conversation data after 30 minutes
    time.sleep(1800)  # 30 minutes
    context.user_data.clear()

def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FILE_UPLOAD: [MessageHandler(filters.Document, handle_document)],
        FILE_CONFIRM: [MessageHandler(filters.Text, done)],
    },
    fallbacks=[CommandHandler('start', start)]
)

