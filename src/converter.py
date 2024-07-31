from moviepy.editor import VideoFileClip
import io

def convert_video_to_audio(video_data: io.BytesIO, output_format='mp3') -> io.BytesIO:
    video = VideoFileClip(io.BytesIO(video_data.read()))
    audio_io = io.BytesIO()
    video.audio.write_audiofile(audio_io, codec='pcm_s16le' if output_format == 'wav' else None)
    audio_io.seek(0)  # Переместим указатель в начало файла
    return audio_io
