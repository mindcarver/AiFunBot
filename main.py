import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from config import TOKEN
from handlers.start import start


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



def main() -> None:
    """Start the bot."""
    logging.info("Starting bot...")
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
