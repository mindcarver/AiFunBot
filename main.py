import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from config import TOKEN
from handlers.start import start
from handlers.button_callback import button_callback
from handlers.generator import handle_image_generation
from constant import IMAGE_GENERATION


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)





def main() -> None:
    """Start the bot."""
    logging.info("Starting bot...")
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler("start", start)

    ## 创建会话处理器
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback)], ## 对话入口
        states={
            IMAGE_GENERATION: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    handle_image_generation
                )
            ],
        },
        fallbacks=[],
    )
    application.add_handler(start_handler)
    ## application.add_handler(CallbackQueryHandler(button_callback)) ## 这个会影响下面的会话内容，不会生效
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
