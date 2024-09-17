

![Landing Page](https://github.com/mflvn/IC_DeepSearch_Vercel/assets/23427834/7ce6b556-ac6c-456e-95e3-a7e7730bad79)


# Turning PDFs into Engaging Videos

## Introduction

Our PDF to Video Converter is an innovative application designed to transform PDF documents into dynamic, engaging video content with minimal human intervention. This project leverages advanced AI technologies to automate the conversion process, providing a flexible, user-friendly solution that caters to the needs of professionals who require quick summarization and presentation of report contents.


## Motivation
With the advancement of language and image generation models, converting text-based content into videos represents a significant leap forward in content consumption. This technology not only aids in rapid information processing but also enhances the accessibility and appeal of textual data. Our project was inspired by the potential to fill a gap in current technology, as exemplified by OpenAI's state-of-the-art text-to-video generation model, [Sora](https://openai.com/sora), which is not yet publicly available.

Our application guides users through a straightforward process, from uploading PDFs to generating a final video. The interface is designed to be intuitive, allowing users to make selections that influence the style and content of the generated video.

## Overview

In collaboration with DeepSearch Labs, we developed a robust "pipeline" approach to generate videos from PDF files. Our process includes:

- Parsing the PDF
- Extracting relevant topics
- Scriptwriting based on extracted content
- Generating corresponding images
- Selecting relevant stock videos
- Narrating the video
- Compiling and animating the components into a final video product

![Upload PDF](https://github.com/mflvn/IC_DeepSearch_Vercel/assets/23427834/c2cc59c4-341b-4885-8161-95f4e048b68e)
![Edit Video Length](https://github.com/mflvn/IC_DeepSearch_Vercel/assets/23427834/198297f0-0f95-4e7a-bee8-f03921b840d1)
![Choose voice](https://github.com/mflvn/IC_DeepSearch_Vercel/assets/23427834/ef815b80-bf1c-447a-889a-e6eaa549feb1)
![Choose script style](https://github.com/mflvn/IC_DeepSearch_Vercel/assets/23427834/f77a2753-2550-4731-8f43-39a3c8c207c9)

## Tech Stack

### Frameworks

- [Next.js](https://nextjs.org/) – React framework for building performant apps with the best developer experience

### Platforms

- [Vercel](https://vercel.com/) – Easily preview & deploy changes with git, robust support for deploying web applications.

### UI

- [Tailwind CSS](https://tailwindcss.com/) – Utility-first CSS framework for rapid UI development
- [HeadlessUI](https://headlessui.com/) - Completely unstyled, fully accessible UI components, designed to integrate beautifully with Tailwind CSS

### Code Quality

- [TypeScript](https://www.typescriptlang.org/) – Static type checker for end-to-end typesafety
- [Python](https://www.python.org/) - All API calls and AI model usage were run in Python scripts integrated into our Next.js UI

## Usage

Active Development Branch: The primary branch for ongoing development is `main`. Contributors should clone and make pull requests to this branch.

### Folder Structure:
```
├── Dockerfile
├── LICENSE.md
├── README.md
├── api
│   ├── add_audio_subtitles.py
│   ├── animate_video_clips.py
│   ├── background_music.py
│   ├── generate_images.py
│   ├── generate_prompts.py
│   ├── pdf_parser.py
│   ├── script_generation.py
│   ├── subtitles_imageprompts.py
│   ├── text_to_speech.py
│   ├── topic_extraction.py
│   ├── tts.py
│   ├── utils.py
│   ├── video_generation.py
│   ├── video_generation_helper.py
│   └── video_with_subtitles.py
├── app
├── components
├── next.config.js
├── package-lock.json
├── package.json
├── pnpm-lock.yaml
├── public
├── requirements.txt
├── screenshots
├── styles
│   └── globals.css
├── tailwind.config.js
├── tests
│   ├── test_add_background_music.py
│   ├── test_animate_video_clips.py
│   ├── test_generate_prompts.py
│   ├── test_pdf_parser.py
│   └── test_topic_extraction.py
├── tsconfig.json
└── utils
    └── OpenAIStream.ts
```
Below is an overview of the main folders in this project:

- `/api`: Python scripts for backend API functionality.
- `/components`: React components used across the application.
- `/public`: Static assets like images and fonts, plus files that are displayed on the UI, like music samples and the final video.
- `/tests`: Test scripts.
- `Dockerfile `: Build an image to run a Docker container.
- `requirements.txt`: Necessary installations.

### Running on Docker: 

This software is deployed on Docker. There are two options to run it.

Option 1: You can run a ready-built Docker image by following the instructions below: 
1. Have the Docker app running on your computer
2. Navigate to https://hub.docker.com/r/mflvn/deepsearch
3. In your terminal (in your desired directory) run the "Docker Pull Command" displayed (this should be "docker pull mflvn/deepsearch")
4. Once the image has been pulled, run it with the following command: docker run --rm -it -p 8080:8080/tcp mflvn/deepsearch:latest
5. The software will run on http://localhost:8080/demo

Option 2: You can build and run the Docker image on your computer, please follow the instructions below:
1. Have the Docker app running on your computer
2. Pull the repository from the 'main' GitHub branch
3. In your terminal, navigate to the project folder (the folder where the Dockerfile lives)
4. Run the following command to build the image: docker build --pull --rm -f "Dockerfile" -t icdeepsearchvercel:latest "."
5. Once the image has been built, run it with the following command: docker run --rm -it -p 8080:8080/tcp icdeepsearchvercel:latest
6. The software will run on http://localhost:8080

### Using the application

Click "Try it out" on the landing page and a page with 8 steps will be displayed. Please follow these instructions at each step:

1. "Upload a PDF Report": Upload your file. IMPORTANT - please wait for the parsed text to show up on the right before clicking Continue.
2. "Choose video length": Select one of the three lengths and click continue.
3. "Choose your voiceover speaker": Select one of the four voices. You can sample each voice. Then click continue.
4. "Choose your script style": Select one of the three script styles. Then click continue.
5. "Choose your background music style": Select one of the three music styles. You can sample each music. Then click continue.
6. "Choose your topics": Select the topics you wish to focus on in the video script. You may select multiple. Then click continue.
7. "Edit your script": Wait for the script to load and be displayed. You may regenerate the script and choose between different versions. You may also edit the script directly. Once you are happy with your script, please click continue.
8. "Video generation": Your video is being created. Please allow time for the video to be generated and do not press "Previous Step" or refresh the page until the video is created.

## Tools and APIs
- [OpenAI API](https://platform.openai.com/docs/guides/text-generation): We used the OpenAI API for natural language processing tasks, including text summarization, topic extraction, and script generation. OpenAI's models are highly sophisticated, offering reliable and high-quality outputs that are crucial for generating accurate and engaging scripts based on the PDF content.
- [Pexels API](https://www.pexels.com/api/): The Pexels API was used to fetch high-quality stock videos that are relevant to the content generated from the PDFs. Pexels provides a vast library of free-to-use videos, which enhances the visual appeal of the final video product without incurring additional costs for stock footage.
- [ElevenLabs TTS API](https://elevenlabs.io/docs/api-reference/getting-started): This API converts the generated scripts into clear and natural-sounding audio, which serves as the narration for the videos. ElevenLabs offers one of the most natural-sounding text-to-speech services available, making the video content more accessible and enjoyable for the audience.
- [DALL-E API by OpenAI](https://platform.openai.com/docs/guides/images/image-generation): Used for generating images from text descriptions derived from the video script. DALL-E excels in creating vivid, contextually appropriate images that significantly enhance the visual storytelling aspect of the videos.
- [MoviePy](https://pypi.org/project/moviepy/): MoviePy is a powerful tool that we used for video editing tasks such as merging video clips, adding audio tracks, and applying various video effects. MoviePy is flexible and robust, suitable for automating complex video production processes in our application, which simplifies the rendering of the final video outputs.

## Contributing to Our Project
### Work in Progress

This project is currently a work in progress. We are constantly refining our processes and enhancing the functionality of our PDF to Video application. As we integrate more advanced features and optimize existing workflows, there may be frequent updates and changes.

### How You Can Help
We warmly welcome contributions from the community! Whether you have ideas for new features, notice a bug, or can improve an existing feature, your help would be greatly appreciated.

If you're interested in contributing, please take a look at the following steps:

- **Check the Issues**: Look through our issues tab on GitHub to find tasks that need help or submit a new issue if you have a suggestion or have found a bug.
- **Fork and Clone**: Fork the repository, clone it to your local machine, and switch to the docker branch to start making your changes (`git checkout docker`).
- **Make Your Changes**: Implement your features or fixes in a dedicated branch based on docker.
- **Submit a Pull Request**: After pushing your changes to your fork, submit a pull request to our docker branch for review.

#### Need Help?
If you're unsure where to start or have any questions about contributing, please don't hesitate to reach out by opening an issue or contacting one of our project maintainers directly.

## Authors

- Maria Lovin ([@mflvn](https://github.com/mflvn))
- Anjali Ramesh ([@anjaliramesh42](https://github.com/AnjaliRamesh42))
- Andreea Bacalum ([@andreeabacalum](https://github.com/andreeabacalum))
- Matthew Murphy ([@smugglervt000](https://github.com/smugglervt000))
- Shaun Lin ([@hellisini](https://github.com/Hellisini))

