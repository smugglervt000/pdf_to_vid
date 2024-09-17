from tts import text_to_speech
from generate_prompts import generate_prompts
from generate_images import generate_download_images
from animate_video_clips import animate
from add_audio_subtitles import add_audio_to_video, add_interactive_subtitles
from background_music import add_background_music
import moviepy.editor as mpy
from moviepy.editor import VideoFileClip, CompositeVideoClip
import json
import subprocess
import whisper
from utils import get_new_filename


def transcribe_and_extract_timestamps(audio_path):
    """Transcribes an audio file and extracts the timestamps of each word."""

    # Load the pre-trained Whisper model
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, verbose=False)

    words_with_timestamps = []

    for segment in result["segments"]:
        words_with_timestamps.append(
            {"text": segment["text"], "start": segment["start"], "end": segment["end"]}
        )

    return words_with_timestamps


def get_audio_duration(audio_file_path):
    """Returns the duration of an audio file in seconds."""

    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        audio_file_path,
    ]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return float(result.stdout.strip())


def stitch_videos(video_paths, output_video_path):
    """Stitches together a list of video paths into a single video file."""

    clips = [mpy.VideoFileClip(video) for video in video_paths]
    final_clip = mpy.concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")


if __name__ == "__main__":
    """Main script to generate a video from a script."""

    # Define API keys
    pexels_api_key = "YOUR API KEY"
    tts_api_key = "YOUR API KEY"

    # Get the current directory and new filenames
    current_directory, new_filename, new_log_filename = get_new_filename("script")

    # root is current_directory without api
    root = current_directory.replace("api", "")

    # Define file paths
    subtitles_file = f"{current_directory}/outputs/subtitle.txt"
    prompts_file = f"{current_directory}/outputs/prompts_list.txt"
    user_selections = f"{current_directory}/outputs/selected.json"
    wav_subtitles = f"{current_directory}/outputs/wav_subtitles.wav"
    mp3_subtitles = f"{current_directory}/outputs/mp3_subtitles.mp3"
    ready_script = f"{current_directory}/outputs/readyScript.txt"
    stitched_effect_video_path = (
        f"{current_directory}/outputs/stitched_effect_video.mp4"
    )
    subtitles_no_bg_path = f"{current_directory}/outputs/final_video.mp4"

    # Load the music and voice selected by the user
    with open(user_selections, "r") as file:
        data = json.load(file)

    music = int(data["selectedMusic"]["id"])
    voice_selection = int(data["selectedVoice"]["id"])-1
    voice_options = ["female_gb","female_us","male_gb","male_us"]
    voice = voice_options[voice_selection]

    # Load the subtitles
    with open(subtitles_file, "r", encoding="utf-8") as f:
        subtitles = f.read()

    # Convert the subtitles to speech
    text_to_speech(subtitles, voice, current_directory, tts_api_key)

    # Convert the speech to audio
    words_with_timestamps = transcribe_and_extract_timestamps(wav_subtitles)

    video_length = get_audio_duration(wav_subtitles)
    num_image_prompts = int(video_length // 7)

    with open(ready_script, "r") as file:
        script = file.read()
    generate_prompts(script, num_image_prompts, current_directory)

    # Open the file and load each line into a list
    prompts_list = []
    with open(prompts_file, "r") as file:
        for line in file:
            prompts_list.append(line.strip())

    downloaded_image_filenames = generate_download_images(
        prompts_list, num_image_prompts, current_directory
    )

    effect_video_filenames = animate(
        downloaded_image_filenames, prompts_list, pexels_api_key, current_directory
    )

    stitch_videos(effect_video_filenames, stitched_effect_video_path)

    add_audio_to_video(
        stitched_effect_video_path,
        wav_subtitles,
        f"{current_directory}/outputs/final_video_with_audio.mp4",
    )

    add_interactive_subtitles(
        f"{current_directory}/outputs/final_video_with_audio.mp4",
        mp3_subtitles,
        current_directory,
    )

    add_background_music(music, subtitles_no_bg_path, root)