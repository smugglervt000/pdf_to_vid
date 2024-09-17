import moviepy.editor as mpy
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from moviepy.video.fx.all import crop
import requests
import re
import random

def download_pexels_video(api_key, query, output_file, video_duration):
    """Downloads a video from Pexels API based on a search query."""

    downloaded_video_urls = set()  # Set to store URLs of downloaded videos
    # Set up the endpoint and parameters for the request
    url = 'https://api.pexels.com/videos/search'
    headers = {'Authorization': api_key}
    params = {'query': query, 'per_page': 5}  # Increased per_page to have more options

    # Make the request to Pexels API
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # This will raise an exception for HTTP errors

    # Extract the video URL from the response
    videos = response.json().get('videos', [])
    if not videos:
        print("No videos found.")
        return

    video_url = None
    for video in videos:
        url = video['video_files'][0]['link']
        if url not in downloaded_video_urls:
            video_url = url
            downloaded_video_urls.add(video_url)  # Add to the set to mark as downloaded
            break

    if not video_url:
        print("All videos on this page have already been downloaded.")
        return

    # Download the video
    video_response = requests.get(video_url)
    video_response.raise_for_status()  # This will raise an exception for HTTP errors
    
    # Save the video to a temporary file
    temp_file = 'temp_video.mp4'
    with open(temp_file, 'wb') as f:
        f.write(video_response.content)
    print(f"Video successfully downloaded to {temp_file}")

    # Load the video using MoviePy
    clip = VideoFileClip(temp_file)
    clip = clip.resize((1024, 1024))

    if clip.duration > video_duration:
        clip = clip.subclip(0, video_duration)
        print(f"Video trimmed to {video_duration} seconds.")
        
    # Write the resized video to the output file
    clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

    # Close the clip to free up resources
    clip.close()

    return output_file

def extract_number(filename):
    """Extracts a number from a filename using regular expressions."""

    num = re.findall(r'\d+', filename)
    return int(num[0]) if num else None

def create_zoom_video(image_path, output_path, duration, zoom_point="right"):
    """Creates a zoom-in effect video from an image."""

    size = (1020, 1080)

    # Load the image and set the duration and frame rate
    slide = mpy.ImageClip(image_path).set_fps(25).set_duration(duration).resize(size)

    slide = slide.resize(lambda t: 1 + 0.04 * t)  # Zoom-in effect
    slide = slide.set_position((zoom_point, 'center'))
    slide = mpy.CompositeVideoClip([slide], size=size)

    slide.write_videofile(output_path)

def create_pan_video(image_path, output_video_path, direction, duration, fps=30, resolution=(1020, 1080)):
    """Creates a video with a panning effect from an image."""

    image = ImageClip(image_path, duration=duration)

    # Resize the image to match the video width while maintaining the aspect ratio
    if image.w > image.h:  # Wider image
        image = image.resize(width=resolution[0])
    else:  # Taller or square image
        image = image.resize(height=resolution[1])

    scaled_width = image.size[0]
    scaled_height = image.size[1]
    video_width = resolution[0]
    video_height = resolution[1]

    max_vertical_movement = 60
    # max_horizontal_movement = 60
    max_horizontal_movement = scaled_width - video_width

    if direction == "up":
        # Calculate the starting vertical position for an upward pan
        start_pos = lambda t: ('center', -max_vertical_movement + (max_vertical_movement * t / duration))
    elif direction == "down":
        # For downward movement or any other direction specified
        start_pos = lambda t: ('center', 0 - (max_vertical_movement * t / duration))
    elif direction == "right":
        # Calculate the starting vertical position for an upward pan
        # It needs to start lower (more negative) and move upward towards 0 over the duration
        start_pos = lambda t: (-max_horizontal_movement + (max_horizontal_movement * t / duration), 'center')
    elif direction == "left":
        # For downward movement or any other direction specified
        start_pos = lambda t: (0 - (max_horizontal_movement * t / duration), 'center')

    image = image.set_position(start_pos)
    image.fps = fps

    composite = CompositeVideoClip([image], size=resolution)
    composite.write_videofile(output_video_path, fps=fps)

def crossfade_videos(video_path1, video_path2, crossfade_duration):
    """ Creates a new video by crossfading between two input videos."""

    # Load the video clips
    clip1 = VideoFileClip(video_path1)
    clip2 = VideoFileClip(video_path2)

    # Set the start time for the second clip so that it starts before the first ends,
    # creating the overlap for crossfade
    clip2 = clip2.set_start(clip1.duration - crossfade_duration)

    # Use crossfadein to make the transition smoother
    clip2 = clip2.crossfadein(crossfade_duration)

    # Create a composite video clip
    final_clip = CompositeVideoClip([clip1, clip2])

    return final_clip

def animate(downloaded_image_filenames, prompts_list, pexels_api_key, current_directory):
    """Animates a list of images and prompts using a random selection of zoom and pan effects"""
    
    effect_video_filenames = []
    
    for i, prompt in enumerate(prompts_list):
        # Download a video from Pexels API every 3rd iteration
        if (i+1) % 3 == 0:
            video_filename = f"{current_directory}/outputs/pexels_video_{i}.mp4"
            download_pexels_video(pexels_api_key, prompt, video_filename, 7)
            video_clip = VideoFileClip(video_filename)
            effect_video_filenames.append(video_filename)
        else:
            directions = ["up", "down", "right", "left"]
            zoom_points = ["center", "right"]
            
            # Extract the number from the image filename
            if i >= 3:
                z = i - (i // 3)
            else:
                z = i

            image_filename = downloaded_image_filenames[z]
            x = extract_number(image_filename)  

            # Select a random direction
            if x % 2 == 0:
                direction = random.choice(directions)
                # Generate a new video filename based on the effect and direction
                pan_video_filename = f"{current_directory}/outputs/effect_video_pan_{direction}_{x}.mp4"

                # Apply the selected effect
                create_pan_video(image_filename, pan_video_filename, direction, 7)

                # Append the new video filename to the list
                effect_video_filenames.append(pan_video_filename)
            else:
                zoom_point = random.choice(zoom_points)
                zoom_video_filename = f"{current_directory}/outputs/effect_video_zoom_in_{x}.mp4"
                create_zoom_video(image_filename, zoom_video_filename, 7, zoom_point)
                effect_video_filenames.append(zoom_video_filename)

    effect_video_filenames = sorted(effect_video_filenames, key=extract_number)
    last_two_videos = effect_video_filenames[-2:]  # This grabs the paths of the last two videos

    # Now you can call 'crossfade_videos' with these paths:
    if len(last_two_videos) == 2:
        crossfaded_clip = crossfade_videos(last_two_videos[0], last_two_videos[1], crossfade_duration=3)  # Assuming 3 seconds crossfade
        crossfaded_clip_path = f"{current_directory}/outputs/crossfaded_video.mp4"
        crossfaded_clip.write_videofile(crossfaded_clip_path, codec='libx264', audio_codec='aac')

        # Now replace the last two videos in your list with the crossfaded video for final stitching
        effect_video_filenames[-2:] = [crossfaded_clip_path]
        
    return effect_video_filenames