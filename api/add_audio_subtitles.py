from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip
import whisper
import os
import json

def add_audio_to_video(video_path, audio_path, output_path):
    """Adds an audio track to a video file and saves it to a specified output path."""
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    video_with_audio = video_clip.set_audio(audio_clip)
    video_with_audio.write_videofile(output_path, codec='libx264', audio_codec='aac')

def time_to_seconds(time_obj):
    """Converts a time object to seconds."""
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000

def create_subtitle_clips(subtitles, videosize,fontsize=24, font='Arial', color='yellow', debug = False):
    """Creates subtitle clips from a list of subtitle objects."""
    subtitle_clips = []

    # Create a TextClip for each subtitle
    for subtitle in subtitles:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time

        video_width, video_height = videosize

        text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color, bg_color = 'black',size=(video_width*3/4, None), method='caption').set_start(start_time).set_duration(duration)
        subtitle_x_position = 'center'
        subtitle_y_position = video_height * 4 / 5

        # Set the position of the subtitle
        text_position = (subtitle_x_position, subtitle_y_position)
        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips

def split_text_into_lines(data):
    """Splits a list of words into lines based on a maximum number of characters and duration."""

    MaxChars = 80
    #maxduration in seconds
    MaxDuration = 3.0
    MaxGap = 1.5

    subtitles = []
    line = []
    line_duration = 0
    line_chars = 0

    # Split the words into lines based on the maximum number of characters and duration
    for idx,word_data in enumerate(data):
        word = word_data["word"]
        start = word_data["start"]
        end = word_data["end"]

        line.append(word_data)
        line_duration += end - start

        temp = " ".join(item["word"] for item in line)

        new_line_chars = len(temp)

        # Check if the line exceeds the maximum number of characters or duration
        duration_exceeded = line_duration > MaxDuration
        chars_exceeded = new_line_chars > MaxChars
        if idx>0:
          gap = word_data['start'] - data[idx-1]['end']

          maxgap_exceeded = gap > MaxGap
        else:
          maxgap_exceeded = False

        # If the line exceeds the maximum number of characters or duration, or the maximum gap between words is exceeded, add the line to the subtitles list
        if duration_exceeded or chars_exceeded or maxgap_exceeded:
            if line:
                subtitle_line = {
                    "word": " ".join(item["word"] for item in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "textcontents": line
                }
                subtitles.append(subtitle_line)
                line = []
                line_duration = 0
                line_chars = 0

    # Add the last line to the subtitles list
    if line:
        subtitle_line = {
            "word": " ".join(item["word"] for item in line),
            "start": line[0]["start"],
            "end": line[-1]["end"],
            "textcontents": line
        }
        subtitles.append(subtitle_line)

    return subtitles

def create_caption(textJSON, framesize, fontsize=33, color='white', bgcolor='blue'):
    """Creates a caption from a JSON object containing text and timestamps."""

    wordcount = len(textJSON['textcontents'])
    full_duration = textJSON['end']-textJSON['start']

    word_clips = []
    xy_textclips_positions =[]

    x_pos = 4
    y_pos = 20

    frame_width = framesize[0]
    frame_height = framesize[1]
    x_buffer = frame_width*1/10
    y_buffer = frame_height*1/1.2

    space_width = ""
    space_height = ""

    # Create a TextClip for each word in the textJSON, and add it to the word_clips list
    for index,wordJSON in enumerate(textJSON['textcontents']):
      duration = wordJSON['end']-wordJSON['start']
      word_clip = TextClip(wordJSON['word'], fontsize=fontsize, color=color).set_start(textJSON['start']).set_duration(full_duration)
      word_clip_space = TextClip(" ", fontsize=fontsize, color=color).set_start(textJSON['start']).set_duration(full_duration)
      word_width, word_height = word_clip.size
      space_width,space_height = word_clip_space.size
      if x_pos + word_width+ space_width > frame_width-2*x_buffer:

            #we move to the next line
            x_pos = 0
            y_pos = y_pos+ word_height+20

            # Store info of each word_clip created
            xy_textclips_positions.append({
                "x_pos":x_pos+x_buffer,
                "y_pos": y_pos+y_buffer,
                "width" : word_width,
                "height" : word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration
            })

            word_clip = word_clip.set_position((x_pos+x_buffer, y_pos+y_buffer))
            word_clip_space = word_clip_space.set_position((x_pos+ word_width +x_buffer, y_pos+y_buffer))
            x_pos = word_width + space_width
      else:
            # Store info of each word_clip created
            xy_textclips_positions.append({
                "x_pos":x_pos+x_buffer,
                "y_pos": y_pos+y_buffer,
                "width" : word_width,
                "height" : word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration
            })

            word_clip = word_clip.set_position((x_pos+x_buffer, y_pos+y_buffer))
            word_clip_space = word_clip_space.set_position((x_pos+ word_width+ x_buffer, y_pos+y_buffer))

            x_pos = x_pos + word_width+ space_width


      word_clips.append(word_clip)
      word_clips.append(word_clip_space)

    # Highlight the words in the textJSON
    for highlight_word in xy_textclips_positions:

      word_clip_highlight = TextClip(highlight_word['word'],  fontsize=fontsize, color='blue').set_start(highlight_word['start']).set_duration(highlight_word['duration'])
      word_clip_highlight = word_clip_highlight.set_position((highlight_word['x_pos'], highlight_word['y_pos']))
      word_clips.append(word_clip_highlight)

    return word_clips

def add_interactive_subtitles(filepath, audiofilename, current_directory):
    """Adds interactive subtitles to a video file based on a transcript of the audio."""

    videofilename = filepath

    model = whisper.load_model("medium")
    result = model.transcribe(audiofilename,word_timestamps=True)

    wordlevel_info = []

    #Extract word-level timestamps from the result
    for each in result['segments']:
      words = each['words']
      for word in words:
        wordlevel_info.append({'word':word['word'].strip(),'start':word['start'],'end':word['end']})

    #Store word-level timestamps into JSON file
    with open('data.json', 'w') as f:
        json.dump(wordlevel_info, f,indent=4)

    with open('data.json', 'r') as f:
        wordlevel_info_modified = json.load(f)

    # Split the word-level timestamps into line-level timestamps
    linelevel_subtitles = split_text_into_lines(wordlevel_info_modified)

    for line in linelevel_subtitles:
      json_str = json.dumps(line, indent=4)

    frame_size = (1080,1080)

    all_linelevel_splits=[]

    # Create a caption for each line in the linelevel_subtitles
    for line in linelevel_subtitles:
      out = create_caption(line,frame_size)
      all_linelevel_splits.extend(out)

    bgcolor = (50,50,50)
    # we load the input video
    input_video = VideoFileClip(videofilename)
    # Get the duration of the input video
    input_video_duration = input_video.duration
    #creating a grey box around the subtitles
    bg_width = frame_size[0]  # Span the full width of the video
    bg_height = int(frame_size[1] // 5.8)
    bg_position = (0, frame_size[1] - bg_height)  # position it at the bottom of the video

    bgcolor = (50, 50, 50)  # Background color

    background_clip = ColorClip(size=(bg_width, bg_height), color=bgcolor + (int(255 * 0.8),), ismask=False).set_duration(input_video_duration).set_position(bg_position)

    # we overlay the videos
    final_video = CompositeVideoClip([input_video] +[background_clip]+ all_linelevel_splits)

    # Set the audio of the final video to be the same as the input video
    final_video = final_video.set_audio(input_video.audio)

    final_video.write_videofile(f"{current_directory}/outputs/final_video.mp4", codec='libx264', audio_codec='aac')