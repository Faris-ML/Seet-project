from telegram import Update
from telegram.ext import ApplicationBuilder,ContextTypes,Updater, CommandHandler, MessageHandler, filters, CallbackContext
import requests
from config import TELEGRAM_TOKEN
import logging
import io
import json
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
TOKEN = TELEGRAM_TOKEN  # Replace with your token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! Send me a voice message, and I will tell if it is an AI or human voice."
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
# def start(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /start is issued."""
#     update.message.reply_text('Hi! Send me a voice message, and I will tell if it is an AI or human voice.')

# def echo(update: Update, context: CallbackContext) -> None:
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)

async def handle_voice(update: Update, context: CallbackContext) -> None:
    """Handle voice messages."""
    voice_file = await context.bot.getFile(update.message.voice.file_id)
    out = io.BytesIO()
    out.seek(0)
    await voice_file.download_to_memory(out)
    headers = {
        'Authorization': 'Token 657eae376aac485a626e72ea6a14738b15ffd9a5',
        'Content-Type': 'audio/x-flac'
        }
    response = requests.post('http://52.212.39.35/predict',headers=headers, data = out.getvalue())
    # print(response.text)
    # Assuming the API returns a text response you want to send back to the user
    res = json.loads(response.text)
    if response.status_code == 200:
        await update.message.reply_text(res['presponse'])
    else:
        await update.message.reply_text('Failed to process voice message.')

def start_bot():
    """Start the bot."""
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    
    application.run_polling()
    # updater = Updater(TOKEN)

    # dp = updater.dispatcher

    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(MessageHandler(filters.text & ~filters.command, echo))
    # dp.add_handler(MessageHandler(filters.voice, handle_voice))

    # updater.start_polling()
    # updater.idle()

if __name__ == '__main__':
    start_bot()
