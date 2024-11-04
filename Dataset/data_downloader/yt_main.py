from Dataset.data_downloader.yt_processor.youtube import Downloader
from Dataset.data_downloader.yt_processor.yt_cutter import AudioSplitter
import os

def process_youtube_videos(youtube_ids_file):
    print("=== Start downloading audio files from YouTube ===")
    downloader = Downloader(youtube_ids_file)
    downloader.download_audio()
    print("=== Downloading audio files from YouTube completed ===\n")

    print("=== Start splitting audio files ===")
    audio_dir = os.path.join('../', 'PIAST_YT', 'audio')
    splitter = AudioSplitter(audio_dir)
    
    for filename in os.listdir(audio_dir):
        if filename.endswith('.mp3'):
            video_id = filename[:-4] 
            print(f"Splitting: {video_id}")
            splitter.split_long_audio(video_id)
    
    print("=== Splitting audio files completed ===\n")

if __name__ == "__main__":
    youtube_ids_file = './file_list/yt_ids.csv'
    process_youtube_videos(youtube_ids_file)