from openai import OpenAI
import requests
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client2 = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))

def download_image(image_url, save_as):
    """Downloads an image from a specified URL and saves it with the given filename."""

    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_as, 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download image.")

def generate_download_images(prompts_list, num_image_prompts, current_directory):
    """Generates and downloads image prompts."""

    downloaded_image_filenames = []

    if num_image_prompts <= 15:

        for i, item in enumerate(prompts_list):
            # Skip every 3rd prompt to avoid video prompts
            if (i+1) % 3 != 0:
                prompt = item + " Please illustrate the image in a photorealistic style."
                response = client2.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
                image_url = response.data[0].url
                image_filename = f"{current_directory}/outputs/image_{i}.png"
                download_image(image_url, image_filename)
                downloaded_image_filenames.append(image_filename)

    elif num_image_prompts <= 21:

        for i, item in enumerate(prompts_list[:15]):
            if (i+1) % 3 != 0:
                prompt = item + " Please illustrate the image in a photorealistic style."
                response = client2.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
                image_url = response.data[0].url
                image_filename = f"{current_directory}/outputs/image_{i}.png"
                download_image(image_url, image_filename)
                downloaded_image_filenames.append(image_filename)

        for i, item in enumerate(prompts_list[15:num_image_prompts]):
            if (i+1) % 3 != 0:
                prompt = item + " Please illustrate the image in a photorealistic style."
                response = client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
                image_url = response.data[0].url
                # continue indexing from previous image number
                v = i+15
                image_filename = f"{current_directory}/outputs/image_{v}.png"
                download_image(image_url, image_filename)
                downloaded_image_filenames.append(image_filename)

    else:

        for i, item in enumerate(prompts_list[:15]):
            if (i+1) % 3 != 0:
                prompt = item + " Please illustrate the image in a photorealistic style."
                response = client2.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
                image_url = response.data[0].url
                image_filename = f"{current_directory}/outputs/image_{i}.png"
                download_image(image_url, image_filename)
                downloaded_image_filenames.append(image_filename)

        for i, item in enumerate(prompts_list[15:22]):
            if (i+1) % 3 != 0:
                prompt = item + " Please illustrate the image in a photorealistic style."
                response = client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
                image_url = response.data[0].url
                x= i+15
                image_filename = f"{current_directory}/outputs/image_{x}.png"
                download_image(image_url, image_filename)
                downloaded_image_filenames.append(image_filename)

        for i, item in enumerate(prompts_list[22:num_image_prompts]):
            if (i+1) % 3 != 0:
                prompt = item + " Please illustrate the image in a photorealistic style."
                response = client2.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
                image_url = response.data[0].url
                z = i+22
                image_filename = f"{current_directory}/outputs/image_{z}.png"
                download_image(image_url, image_filename)
                downloaded_image_filenames.append(image_filename)

    return downloaded_image_filenames