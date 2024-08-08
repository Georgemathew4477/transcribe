import speech_recognition as sr
from moviepy.editor import AudioFileClip

from moviepy.editor import AudioFileClip

def convert_video_to_audio(video_file, audio_file):
    # Use moviepy to extract audio file from the video file
    audioclip = AudioFileClip(video_file)
    audioclip.write_audiofile(audio_file)

# Use the function to convert video to audio
video_file = "24-04-23 (Hindi + Eng).mp4"  # Replace with your video file path
audio_file = "output_audio.wav"  # The audio file will be saved with this name
convert_video_to_audio(video_file, audio_file)
