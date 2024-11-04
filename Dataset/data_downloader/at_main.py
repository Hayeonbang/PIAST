import os
import pandas as pd
import librosa
import soundfile as sf
from dataset.data_downloader.yt_processor.youtube import Downloader
from dataset.data_downloader.yt_processor.yt_cutter import AudioSplitter

class AudioTimeSplitter:
    def __init__(self, time_info_file):
        self.time_info_file = time_info_file
        self.source_audio_dir = os.path.join('../', 'PIAST_YT', 'audio')
        self.target_audio_dir = os.path.join('../', 'PIAST_AT', 'audio')
        self.segment_duration = 30  # 30 seconds    

    def create_target_directory(self):
        if not os.path.exists(self.target_audio_dir):
            os.makedirs(self.target_audio_dir)
        if not os.path.exists(self.source_audio_dir):
            os.makedirs(self.source_audio_dir)

    def download_and_process_missing_audio(self, video_id):
        print(f"Attempting to download missing audio for {video_id}")

        downloader = Downloader(None)
        downloader.audio_dir = self.source_audio_dir
        downloader._download_audio(video_id)
        
        source_file = os.path.join(self.source_audio_dir, f"{video_id}.mp3")
        if not os.path.exists(source_file):
            return False
            
        print(f"Splitting long audio for {video_id}")
        splitter = AudioSplitter(self.source_audio_dir)
        splitter.split_long_audio(video_id)
        
        return True

    def load_time_info(self):
        df = pd.read_csv(self.time_info_file)
        return df[['yt_id', 'start_time(seconds)']]

    def process_audio_files(self, auto_download=True):
        self.create_target_directory()
        time_info = self.load_time_info()
        
        total_files = len(time_info)
        skipped_files = []
        
        for idx, row in time_info.iterrows():
            video_id = row['yt_id'][:11]
            start_time = row['start_time(seconds)']
            
            print(f"Processing {idx + 1}/{total_files}: {video_id}")
            
            source_file = os.path.join(self.source_audio_dir, f"{video_id}.mp3")
            target_file = os.path.join(self.target_audio_dir, f"{video_id}.mp3")
            
            if not os.path.exists(source_file):
                if auto_download:
                    print(f"Source file not found. Attempting to download and process...")
                    if not self.download_and_process_missing_audio(video_id):
                        print(f"Failed to download audio for {video_id}")
                        skipped_files.append((video_id, "download_failed"))
                        continue
                else:
                    print(f"Source file not found: {source_file}")
                    skipped_files.append((video_id, "file_not_found"))
                    continue
                
            if os.path.exists(target_file):
                print(f"Target file already exists: {target_file}")
                continue
                
            try:
                audio, sr = librosa.load(source_file, sr=None)
                total_duration = len(audio) / sr
                
                if start_time >= total_duration:
                    print(f"Start time ({start_time:.2f}s) exceeds audio duration ({total_duration:.2f}s)")
                    skipped_files.append((video_id, "invalid_start_time"))
                    continue
                
                start_sample = int(start_time * sr)
                end_sample = start_sample + int(self.segment_duration * sr)
                
                if end_sample > len(audio):
                    available_duration = (len(audio) - start_sample) / sr
                    segment = audio[start_sample:]
                else:
                    segment = audio[start_sample:end_sample]
                
                sf.write(target_file, segment, sr)
                print(f"Successfully created: {target_file}")
                
            except Exception as e:
                print(f"Error processing {video_id}: {str(e)}")
                skipped_files.append((video_id, f"error: {str(e)}"))
        
        print("\n=== Processing Summary ===")
        print(f"Total files processed: {total_files}")
        print(f"Files skipped: {len(skipped_files)}")
        
        if skipped_files:
            print("\nSkipped files details:")
            for video_id, reason in skipped_files:
                print(f"- {video_id}: {reason}")

def main():
    time_info_file = './file_list/at_time_info.csv'
    splitter = AudioTimeSplitter(time_info_file)
    splitter.process_audio_files(auto_download=True)

if __name__ == "__main__":
    main()