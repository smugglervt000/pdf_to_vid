from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeAudioClip
import os

def add_background_music(option, video_file, root):
    """Adds background music to a video file and saves it to a specified output path."""

    video_clip = VideoFileClip(video_file)

    # Load the background music based on the option
    if option == 1:
        background_music_clip = AudioFileClip(root+'/api/outputs/background_music_subtle.mp3').volumex(0.2)
    if option == 2:
        background_music_clip = AudioFileClip(root+'/api/outputs/background_music_energetic.mp3').volumex(0.1)
    if option == 3:
        background_music_clip = AudioFileClip(root+'/api/outputs/background_music_formal.mp3').volumex(0.2)

    # Repeat the background music to cover the whole video
    number_of_repeats = video_clip.duration / background_music_clip.duration + 1  # Add 1 to ensure it covers the whole video
    background_music_clips = [background_music_clip] * int(number_of_repeats)

    long_background_music_clip = concatenate_audioclips(background_music_clips)

    # shorten background music clip to match the video's duration
    long_background_music_clip = long_background_music_clip.subclip(0, video_clip.duration)

    original_audio_clip = video_clip.audio

    # mixing the original audio with the background music
    mixed_audio_clip = CompositeAudioClip([original_audio_clip.volumex(1.0), long_background_music_clip])  # Adjust original audio volume

    # we set the mixed audio as the audio of the original video clip
    video_clip_with_new_audio = video_clip.set_audio(mixed_audio_clip)

    #final video with background music
    video_clip_with_new_audio.write_videofile(root + "/public/final_merged_video.mp4", codec='libx264', audio_codec='aac')

    video_clip.close()
    background_music_clip.close()
    original_audio_clip.close()
    mixed_audio_clip.close()
    long_background_music_clip.close()
    # rename the final video file
    os.rename(root + "/public/final_merged_video.mp4", root + "/public/final.mp4")