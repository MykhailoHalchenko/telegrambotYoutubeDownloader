import yt_dlp
import os
import time

def download_video(url):
    temp_file = 'temp_video.mp4'
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': temp_file,
        'noplaylist': True,
        'retries': 3,  
        'retry_sleep': 5,  
        'timeout': 60  
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', 'video')
            ext = info_dict.get('ext', 'mp4')
            
            video_path = f"{title}.{ext}"
            os.rename(temp_file, video_path)
    except Exception as e:
        raise RuntimeError(f"Error downloading video: {e}")

    return video_path, title
