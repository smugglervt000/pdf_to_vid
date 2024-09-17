import shutil
import fitz
import re
import sys
import os
from utils import get_new_filename


def parse(filepath):
    """Parse text from a PDF file."""

    document = fitz.open(filepath)
    text_list = []

    # Extract text from each page
    for page_num in range(len(document)):
        page = document.load_page(page_num)

        page_text = page.get_text()
        text_list.append(page_text)

    document.close()

    # Clean text
    text = " ".join(text_list)
    text = text.replace("-\n", "")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    url_pattern = r"https?://\S+|www\.\S+"
    text = re.sub(url_pattern, "", text)

    return text


if __name__ == "__main__":
    filepath = sys.argv[1]
    text = parse(filepath)

    # Get the current directory and new filenames
    current_directory, new_filename, new_log_filename = get_new_filename("parse")
    source_file = current_directory + " /public/final.mp4"
    destination_file = current_directory + "/logs/final_merged_video.mp4"
    if os.path.exists(source_file):
        shutil.move(source_file, destination_file)

    # Save the parsed text to a new file
    with open(new_log_filename, "w") as file:
        file.write(text)
    with open(new_filename, "w") as file:
        file.write(text)