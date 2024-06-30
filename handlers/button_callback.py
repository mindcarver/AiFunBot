from telegram import Update
from telegram.ext import CallbackContext
from constant import IMAGE_GENERATION


async def button_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    resp_text = "prepare to generate image ,pls write prompt..."
    if query.data == "generate_image":
        await query.edit_message_text(text=resp_text)

    return IMAGE_GENERATION
