from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from downloader import download_video
from converter import convert_video_to_audio
import io
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN_TG_BOT')

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Hi! Send me a link to a YouTube video and I will download it and convert it to audio. '
        'Use /download <YouTube URL> to download a video. After downloading, use /convert <mp3/wav> to convert it.'
    )

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Available commands:\n'
        '/start - Start the bot and get instructions\n'
        '/help - Show this help message\n'
        '/download <YouTube URL> - Download a YouTube video\n'
        '/convert <mp3/wav> - Convert the downloaded video to audio format'
    )

async def download(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        await update.message.reply_text('Please provide a YouTube URL.')
        return
    
    url = context.args[0]
    await update.message.reply_text('Downloading video...')
    
    try:
        video_path, title = download_video(url)
        
        with open(video_path, 'rb') as video_file:
            video_data = video_file.read()
            await update.message.reply_video(video_data, caption=title)
        
        context.user_data['video_data'] = video_data
        context.user_data['title'] = title
        
        os.remove(video_path)
    except Exception as e:
        await update.message.reply_text(f'An error occurred while downloading: {e}')

async def convert(update: Update, context: CallbackContext):
    if 'video_data' not in context.user_data:
        await update.message.reply_text('First you need to download the video. Use the /download command.')
        return
    
    if len(context.args) == 0 or context.args[0] not in ['mp3', 'wav']:
        await update.message.reply_text('Please specify the audio format: /convert <mp3/wav>.')
        return
    
    video_data = context.user_data['video_data']
    title = context.user_data['title']
    audio_format = context.args[0]
    await update.message.reply_text(f'Converting video to audio ({audio_format})...')
    
    try:
        audio_data = convert_video_to_audio(io.BytesIO(video_data), audio_format)
        await update.message.reply_text(f'Audio converted to {audio_format}. Sending file...')
        
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio_data, title=title)
        
        del context.user_data['video_data']
        del context.user_data['title']
    except Exception as e:
        await update.message.reply_text(f'An error occurred while converting: {e}')

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("download", download))
    application.add_handler(CommandHandler("convert", convert))

    application.run_polling()

if __name__ == '__main__':
    main()
