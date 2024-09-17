from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client2 = OpenAI(api_key=os.getenv("OPENAI_API_KEY_2"))

def generate_image_prompts(script, num_image_prompts):
    """API call to generate image prompts from script and number of image prompts."""

    prompt = f"""Here is a script for a video I am making: '{script}' I am using a text to image model to come up with relevant images for the video. 
                Could you please provide {num_image_prompts} prompts to use in the text to image model to get the images for my video? Could you please 
                make sure these prompts encourage the model to generate images capable of telling the same story the script is telling, and that each image
                transitions to the next in a sequence that flows well and makes sense. Remember that these prompts are going to be input one at a time into an 
                independent text to image model, so while each prompt talks about whats important at that part of the video, they need to be able to stand on their 
                own and incorporate the main themes of the script so that the images that are generated don't lose important information. Make sure to be incredibly 
                descriptive (3-5 sentences for each prompt). Make sure to be incredibly thorough and include all of the nouns that you think should be in the image, 
                how the colors should look, etc. The nouns are the most important part, please describe how the nouns should look from the context of the script and
                the story at hand. 

                Use the following template for the response:

                **1. Prompt Title**: Description of the first prompt
                
                **2. Prompt Title**: Description of the second prompt
              
                **n. Prompt Title**: Description of the nth prompt

                Thanks for the help."""

    response = client.chat.completions.create(
            model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are designing image prompts to be input in an AI text to image model"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    image_prompts = response.choices[0].message.content
    return image_prompts

def generate_video_prompts(image_prompt_to_replace, script):
    """API call to generate video prompts from script and number of video prompts"""

    prompt = f"Here is an image prompt that I am feeding into a text to image model to include in a video that I'm creating: {image_prompt_to_replace}. Could you provide a shorter, less detailed version of this prompt to use to find a video? Since the image is being generated, the image prompt can be detailed and descriptive, but I am getting the video by searching for stock footage, so the video prompt should be more general and less detailed. Could you please provide a video prompt that is related to this image prompt and can be used to find stock footage that would be relevant to the image prompt? They should revolve around the same topic as this script that I'm using: {script}. Thanks for the help."

    response = client.chat.completions.create(
            model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are designing image prompts to be input in an AI text to image model"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4

    )

    video_prompt = response.choices[0].message.content

    for section in video_prompt.split('\n\n'):
        if '"' in section:
            # Split by '**' to remove the numeric and title part.
            prompt_description = section.split('"')[1].strip()
            # print("prompt description", prompt_description)
            return prompt_description
        
def generate_prompts(script, num_image_prompts,current_directory):
    """Generates image and video prompts from script and number of image prompts, writes generated prompts to a file"""
    
    image_prompts = generate_image_prompts(script, num_image_prompts)
    # print("image prompts",image_prompts)
    rawfilename = f"{current_directory}/outputs/prompts_list_raw.txt"

    with open(rawfilename, 'w') as file:
        file.write(image_prompts)

    prompts_list = []
    
    # Split the image prompts into a list of prompts, based on markdown formatting of openai response
    lines = image_prompts.split('\n')
    for line in lines:
        if line.startswith('**') and 'Description' in line:
            prompt = line.split('Description**:')[1].strip()
            prompts_list.append(prompt)
        elif line.startswith('**') and 'Description' not in line:
            parts = line.split('**')
            if len(parts) >= 3:
                prompt = parts[2].strip()
                prompts_list.append(prompt)

    # Generate video prompts for every 3rd prompt
    for i in range(2, len(prompts_list), 3):
        video_prompt = generate_video_prompts(prompts_list[i], script)
        prompts_list[i] = video_prompt

    filename = f"{current_directory}/outputs/prompts_list.txt"

    # Write the prompts to a file
    with open(filename, 'w') as file:
        for prompt in prompts_list:
            file.write(prompt + "\n")

    print(f"List has been written to {filename}")