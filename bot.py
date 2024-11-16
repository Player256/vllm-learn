
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "TELEGRAM_BOT_TOKEN"
API_URL = "http://localhost:5000/generate" 

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! I am your AI bot. Send me a prompt, and I'll generate a response for you!"
    )

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_prompt = update.message.text

    try:
        response = requests.post(API_URL, json={"prompt": user_prompt})
        if response.status_code == 200:
            generated_text = response.json().get("response", "No text generated.")
            await update.message.reply_text(generated_text)
        else:
            await update.message.reply_text("API error. Please try again later.")
            logger.error(f"API returned an error: {response.text}")
    except Exception as e:
        await update.message.reply_text("An error occurred while generating text.")
        logger.error(f"Error: {e}")

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))
    application.run_polling()

if __name__ == "__main__":
    main()
