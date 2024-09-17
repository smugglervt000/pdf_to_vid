import json
import requests
from transformers import AutoTokenizer
from transformers import pipeline
from utils import get_new_filename

def text_to_speech(text_input):
    """Converts text to speech."""
    url = "https://api.edenai.run/v2/audio/text_to_speech"

    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "rate": 0,
        "pitch": 0,
        "volume": 0,
        "sampling_rate": 0,
        "providers": "amazon",
        "language": "en",
        "text": text_input,
        # "option": "FEMALE"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "YOUR API KEY",
    }

    response = requests.post(url, json=payload, headers=headers)

    response1 = json.loads(response.text)
    return response1["amazon"]["audio_resource_url"]


if __name__ == "__main__":
    current_directory, new_filename, new_log_filename = get_new_filename("text_to_speech")
    with open(f"{current_directory}/outputs/subtitle.txt", "r") as file:
        ARTICLE = file.read()    
    checkpoint = "t5-small"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    model_name = "pszemraj/long-t5-tglobal-base-sci-simplify"

    summarizer = pipeline("summarization", model=model_name)

    tokens = ARTICLE.split()
    num_tokens = len(tokens)

    preferred_length = 1


    print(text_to_speech(ARTICLE))