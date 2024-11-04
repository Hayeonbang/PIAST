import os
from pydub import AudioSegment

"""
Split long audio files into 10-minute parts.
"""

class AudioSplitter:
    def __init__(self, audio_dir):
        self.audio_dir = audio_dir
        self.long_files_dir = os.path.join(self.audio_dir, 'long_files')

    def split_long_audio(self, video_id):
        audio_file = os.path.join(self.audio_dir, f"{video_id}.mp3")

        if not os.path.exists(self.long_files_dir):
            os.makedirs(self.long_files_dir)

        if not os.path.isfile(audio_file):
            print(f"Audio file for {video_id} does not exist. Skipping splitting.")
            return

        try:
            audio = AudioSegment.from_mp3(audio_file)
            duration_in_ms = len(audio)  
            part_duration = 10 * 60 * 1000  # 10 minutes (milliseconds)

            for i in range(0, duration_in_ms, part_duration):
                part = audio[i:i + part_duration]
                part_file = os.path.join(self.long_files_dir, f"{video_id}_part_{i // part_duration + 1}.mp3")
                part.export(part_file, format="mp3")
                print(f"Exported {part_file}")
            
            print(f"All parts of {video_id} have been processed.")

        except Exception as e:
            print(f"Error splitting audio for {video_id}: {str(e)}")

