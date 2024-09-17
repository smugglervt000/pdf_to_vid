from openai import OpenAI
from utils import get_new_filename
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_topics(topics_string, chosen_numbers):
    """Parse the topics string to extract the chosen topics and keyphrases based on the chosen numbers."""

    chosen_topics = []
    chosen_keyphrases = []

    lines = topics_string.strip().split("\n")

    current_topic_number = 0
    current_topic = ""
    subthemes = []
    collecting_subthemes = False

    # Iterate through the lines to extract the chosen topics and keyphrases
    for line in lines:
        if line and line[0].isdigit():
            # If we start collecting a new topic, check if the last topic was in chosen_numbers
            if collecting_subthemes:
                chosen_topics.append(
                    current_topic.split(": ")[1]
                )  # Only add the topic description
                chosen_keyphrases.append(" ".join(subthemes))
                subthemes = []  # Reset for the next topic
                collecting_subthemes = False

            current_topic_number = int(line.split(":")[0])
            if current_topic_number in chosen_numbers:
                current_topic = line
                collecting_subthemes = True
        
        elif collecting_subthemes and "- (Possible subthemes:" in line:
            # Collect subthemes for the current topic, removing the prefix "Possible subthemes: "
            cleaned_line = line.replace("- (Possible subthemes: ", "").rstrip(")")
            subthemes.append(cleaned_line)

    # Add the last topic if it was chosen and not added yet
    if collecting_subthemes:
        chosen_topics.append(
            current_topic.split(": ")[1]
        )  # Only add the topic description
        chosen_keyphrases.append(" ".join(subthemes))

    return chosen_topics, chosen_keyphrases

def create_summary_for_script(topic, text, keywords):
  """Generate an intermediate summary to summarize the topic selected using the full parsed text"""

  # Convert keywords list to a string
  keywords_str = ", ".join(keywords)

  # Prepare the prompt
  prompt = f"Imagine you are a summarizer. Write a summary of this text: {text}, focused on {topic} as highlighted in the topic discovery output. The main ideas are these key phrases: {keywords_str}. The summary should have a clear explanation of this topic and these key points."
  
  try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": 'Imagine you are a factual summariser.'},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7, # mid-range temperature to facilitate creativity but not hallucination
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        return response.choices[0].message.content.strip()
  
  except Exception as e:
    return f"An error occurred: {str(e)}"


def generate_video_script_singletopic(length, summary, topic, keywords, text, audience, tone):
    """Generate a single topic video script using a selected topic and keywords."""
    
    # Convert keywords list to a string
    keywords_str = ", ".join(keywords)
    # text = text[0:2200]
    num_words = 100
    prompt = ''

    if length == "1min":
        num_words = 120
    elif length == "2min":
        num_words = 240
    elif length == "3min":
        num_words = 360    

    casual_prompt = f'''Imagine you are a script writer. Write a {length}-minute video script, around {num_words} words. Focus on {topic} (and subtopics {keywords_str}), expanding upon this summary: {summary}. This is the original text which you should use to add context to the script: {text}. The script should start with an engaging introduction that captures the audience's interest, followed by a clear explanation of {topic} and {summary}. Conclude with a compelling message that underscores the significance of {topic}. Please ensure the script is suitable for a(n) {audience} audience and matches a {tone} tone. Use the word 'narrator' for any speaking parts. Include highly descriptive image prompts for the video on separate lines, but do not include copyrighted images such as logos, or images of famous people. Enclose image prompts in square brackets []. Exclude words such as 'keywords', 'topic'. Do not include a title.
    
    Use the following template for the response:

    [Highly descriptive image prompt 1]

    Narrator: Script text

    [Highly descriptive image prompt 2]

    Narrator: Script text

    ...
    
    [Highly descriptive image prompt n]

    Narrator: Script text]'''

    formal_prompt = f'''Imagine you are a script writer. Write a {length}-minute video script, around {num_words} words. Focus on the topic {topic} (and subtopics {keywords_str}), expanding upon this summary: {summary}. This is the original text which you should use to add context to the script: {text}. The script should have a formal, business-like style that is ideal for meetings or presentations, and have a concise explanation of {topic} and {summary}. Just report the objective facts in a formal way. Please ensure the script is suitable for a professional audience and matches a formal tone. Use the word 'narrator' for any speaking parts. Include highly descriptive image prompts for the video on separate lines, but do not include copyrighted images such as logos, or images of famous people. Enclose image prompts in square brackets []. Exclude words such as 'keywords', 'topic'. Do not include a title. 
    
    
    Use the following template for the response:

    [Highly descriptive image prompt 1]

    Narrator: Script text

    [Highly descriptive image prompt 2]

    Narrator: Script text

    ...
    
    [Highly descriptive image prompt n]

    Narrator: Script text]'''


    funny_prompt = f'''Imagine you are a script writer. Write a {length}-minute video script, around {num_words} words. Focus on the topic {topic} (and subtopics {keywords_str}), expanding upon this summary: {summary}. This is the original text which you should use to add context to the script: {text}. The script should have a funny, relaxed style that is ideal for friends and family, and have a humorous explanation of {topic} and {summary}. Keep the script concise, and ensure that the script is suitable for a {audience} audience and matches a {tone} tone. Use the word 'narrator' for any speaking parts. Include highly descriptive image prompts for the video on separate lines, but do not include copyrighted images such as logos, or images of famous people. Enclose image prompts in square brackets []. Exclude words such as 'keywords', 'topic'. Do not include a title.
    
    
    Use the following template for the response:

    [Highly descriptive image prompt 1]

    Narrator: Script text

    [Highly descriptive image prompt 2]

    Narrator: Script text

    ...

    [Highly descriptive image prompt n]

    Narrator: Script text]'''
    
    if tone == "Formal":
        prompt = formal_prompt
    elif tone == "Relaxed":
        prompt = casual_prompt
    elif tone == "Funny":
        prompt = funny_prompt

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 'Imagine you are a script writer. Avoid using any content that violates OpenAIs use case policy, such as Copyrighted content.'},
                {"role": "user", "content": prompt}, 
            ],
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        script = response.choices[0].message.content.strip()
    
        return script
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    current_directory, new_filename, new_log_filename = get_new_filename("script")

    with open(f"{current_directory}/outputs/topic.txt", "r") as file:
        content = file.read()
    with open(f"{current_directory}/outputs/parse.txt", "r") as file:
        text = file.read()

    import json

    # Load data from selected.json
    with open(f"{current_directory}/outputs/selected.json", "r") as file:
        data = json.load(file)
    with open(f"{current_directory}/outputs/topic.json", "r") as file:
        all_topics = json.load(file)

    # Extract relevant information from the loaded data
    chosen_topics = data["selectedTopics"]
    # Join all chosen keyphrases into a single string separated by commas
    chosen_keyphrases = [phrase for topic in chosen_topics for phrase in all_topics.get(topic, [])]

    # Get the selected length, audience, and tone
    length = data["selectedLength"]["id"]
    audience = "general public"
    tone = data["selectedStyle"]["name"]

    # Generate a summary for the selected topic
    summary = create_summary_for_script(chosen_topics, text, chosen_keyphrases)
    with open(f"{current_directory}/outputs/summary.txt", "w") as file:
            file.write(summary)

    # Generate the video script
    script = generate_video_script_singletopic(
        length, summary, chosen_topics, chosen_keyphrases, text, audience, tone
    )

    # Write the script to a file
    with open(new_filename, "w") as file:
        file.write(script)
    with open(new_log_filename, "w") as file:
        file.write(script)