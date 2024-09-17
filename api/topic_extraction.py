import json
import os
import re

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import OpenAI
from utils import get_new_filename

def text_to_json(text):
    """Converts a text string to a JSON format."""

    lines = text.split('\n')
    data = {}
    key = ''
    for line in lines:
        if line.strip() == '':
            continue
        if re.match(r'\d+:', line):
            key = line.split(':')[1].strip()
            data[key] = []
        else:
            data[key].append(line.strip('- ').strip())
    return json.dumps(data, indent=4)


def topics_from_text(llm, input_text, num_topics):
    """Extract topics from input text using LLM API call, formatted according to a template."""

    template_string = '''Extract {num_topics} main topics from the following text.
    Then, write down three possible different subthemes for each topic.
    Note that each item should directly convey the idea without using the word 'topic'. Each topic should be unique and not similar to other ones. Remember, the goal is to provide a clear, engaging, and semi-detailed overview of the main subject, then delve into its nuances through the subthemes.
    Use the following template for the response.

    1: Sentence describing the topic 
    - Phrase describing the first subtheme
    - Phrase describing the second subtheme
    - Phrase describing the third subtheme

    ...

    n: Sentence describing the topic
    - Phrase describing the first subtheme
    - Phrase describing the second subtheme
    - Phrase describing the third subtheme

    Here is the text: """{input_text}""" '''

    # LLM call
    prompt_template = ChatPromptTemplate.from_template(template_string)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    formatted_response = chain.run({
        "input_text": input_text,
        "num_topics": num_topics
    })

    # converting formatted response into one long string
    non_formatted_response = formatted_response.replace('\n', ' ').replace(' - ', ', ').replace(':', ',').replace('  ', ' ')

    return formatted_response, non_formatted_response

if __name__ == "__main__":
    current_directory, new_filename, new_log_filename = get_new_filename("topic")
    print("current_directory", current_directory)
    with open(f"{current_directory}/outputs/parse.txt", 'r') as file:
        content = file.read()

    # Parse the first 3500 characters of the text, to account for API limitations
    parsed_pdf_string = content[0:3500]


    openai_key = os.getenv("OPENAI_API_KEY")
    llm = OpenAI(openai_api_key=openai_key)

    num_topics = 4

    # return topics and non_formatted_response in the form of a string
    topics, non_formatted_response = topics_from_text(llm, parsed_pdf_string, num_topics)

    topic_json = text_to_json(topics)

    # Save the topics to a file
    with open(f"{current_directory}/outputs/topic.json", 'w') as topics_file:
        topics_file.write(topic_json)

    with open(new_filename, 'w') as topics_file:
        topics_file.write(topics)
    with open(new_log_filename, 'w') as topics_file:
        topics_file.write(non_formatted_response)