from moviepy.editor import *

def convert_video_to_audio(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path, codec='mp3')
        audio.close()
        video.close()
        print("Conversion successful!")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    input_video_path = "GMT20200606-112116_Batch_2_Wi.m4a"  # Replace this with the path to your video file
    output_audio_path = "GMT20200606-112116_Batch_2_Wi.mp3"  # Replace this with the desired output audio path

    convert_video_to_audio(input_video_path, output_audio_path)
    