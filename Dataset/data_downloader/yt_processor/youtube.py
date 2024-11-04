import os
import yt_dlp as youtube_dl

"""
Download audio files from YouTube.
"""

class Downloader:
    def __init__(self, youtube_ids_file):
        self.youtube_ids_file = youtube_ids_file
        self.audio_dir = os.path.join('../', 'PIAST_YT', 'audio')

    def download_audio(self):
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)

        with open(self.youtube_ids_file, 'r') as file:
            youtube_ids = [line.strip() for line in file]

        for i, video_id in enumerate(youtube_ids, start=1):
            print(f"Processing video {i}/{len(youtube_ids)}: {video_id}")
            self._download_audio(video_id)

    def _download_audio(self, video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"
        audio_file = os.path.join(self.audio_dir, f"{video_id}.mp3")

        if os.path.isfile(audio_file):
            print(f"Audio file for {video_id} already exists. Skipping download.")
            return

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': audio_file,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Audio for {video_id} downloaded successfully.")

        except Exception as e:
            print(f"Error downloading {video_id}: {str(e)}")
