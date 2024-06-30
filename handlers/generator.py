from telegram import Update
from telegram.ext import CallbackContext
from constant import IMAGE_GENERATION
from services.comfyui.comfyui_websocket import get_images_from_comfyui
async def handle_image_generation(update: Update, context: CallbackContext) -> int:
    user_prompt = update.message.text
    await update.message.reply_text(f"Generating image for prompt: {user_prompt}")
    
    ## 这里你可以调用图像生成API或其他逻辑
    img_bytes = get_images_from_comfyui(user_prompt)
    
    ## 发送图片到bot  
    await update.message.reply_photo(photo=img_bytes)
  
    return IMAGE_GENERATION   ## 停留在此状态