#script to generate audio from text using ElevenLabs API

import requests
from elevenlabs import play, save
from elevenlabs.client import ElevenLabs


def text_to_speech(subtitles, voice_choice, current_directory, tts_api_key):
    """Converts text to speech using ElevenLabs API."""

    # Text-to-Speech (TTS) configuration and API call
    voice_id = 'YOUR API KEY'

    female_gb_voice_id = 'FEMALE GB ID'
    male_gb_voice_id = 'MALE GB ID'
    female_us_voice_id = 'FEMALE US ID'
    male_us_voice_id = 'MALE US ID'

    #female british accent
    if voice_choice == "female_gb":
        voice_id = female_gb_voice_id
    #male british accent
    elif voice_choice == 'male_gb':
        voice_id = male_gb_voice_id
    #female american accent
    elif voice_choice == 'female_us':
        voice_id = female_us_voice_id
    #male american accent
    elif voice_choice == 'male_us':
        voice_id = male_us_voice_id


    output_format = 'wav'

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": tts_api_key,
        "Content-Type": "application/json",
        }
    payload = {
        "text": subtitles,
        "model_id": "eleven_turbo_v2",
        "outputFormat": output_format
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # Save the audio file to the outputs folder with a specified output format
    if response.ok:
        with open(f"{current_directory}/outputs/wav_subtitles." + output_format, 'wb') as f:
            f.write(response.content)
        print('The audio file has been saved as .wav')
        
        with open(f"{current_directory}/outputs/mp3_subtitles." + 'mp3', 'wb') as f:
            f.write(response.content)
        print('The audio file has been saved as .mp3')
    else:
        print('Error:', response.text)
 