import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import os
import uuid
import time

logging.basicConfig(level=logging.INFO)

TOKEN = '7167327959:AAFJ25AIsO9olQrSzV2OcM0YqY7yUzWekDQ'
CHANNEL_ID = '-1001329275814'

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
    # Store file data in the channel permanently
    context.bot.send_document(chat_id=CHANNEL_ID, document=file_id)
    update.message.reply_text(f'File link: https://example.com/{file_unique_id}')
    update.message.reply_text('Warning: Your conversation data will be deleted in 30 minutes. Please forward the file to another location to keep it permanently.')
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
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FILE_UPLOAD: [MessageHandler(Filters.document, handle_document)],
            FILE_CONFIRM: [MessageHandler(Filters.text, done)],
        },
        fallbacks=[CommandHandler('start', handle_start)]
    )

    dp.add_handler(conv_handler)

    # Start a separate thread to delete conversation data after 30 minutes
    import threading
    threading.Thread(target=delete_conversation_data, args=(updater.dispatcher.context,)).start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
