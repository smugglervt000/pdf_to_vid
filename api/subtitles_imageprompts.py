import os
from utils import get_new_filename
import re


def extract_subtitles_images(script):
	"""Extracts subtitles and image prompts from a script."""

	subtitles = ""
	image_prompts = ""

	lines = script.split("\n")
	count=0

	# parse each line in the script
	for line in lines:
		if count < 5 and (
			"visuals" in line.lower()
			or "[intro]" in line.lower()
			or "[outro]" in line.lower()
			or "cut to" in line.lower()
			or "shot" in line.lower()
			or line.startswith("[") and line.endswith("]")
		):
			count+=1
			image_prompts += line.strip() + "\n"
		elif "narrator" in line.lower():
			clean_line = re.sub(r'(?i)\*?\*?narrator[\*\*:,]?\*?\*?', '', line).strip()
			subtitles += clean_line + "\n"

	subtitles = subtitles.strip()
	image_prompts = image_prompts.strip()

	return subtitles, image_prompts


if __name__ == "__main__":
	current_directory, new_filename, new_log_filename = get_new_filename("log_SIP")

	with open(f"{current_directory}/outputs/readyScript.txt", "r") as file:
		content = file.read()

	script = content
	cd = os.getcwd()+'/api' if not os.environ.get('DOCKER') else  current_directory
	print(cd)
	print(os.environ.get('DOCKER'))
	subtitles, image_prompts = extract_subtitles_images(script)

	with open(f"{cd}/outputs/subtitle.txt", 'w') as topics_file:
		topics_file.write(subtitles)

	with open(f"{cd}/logs/subtitle.txt", 'w') as topics_file:
		topics_file.write(subtitles)