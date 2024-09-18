import unittest
from unittest.mock import patch, MagicMock
from generate_prompts import generate_image_prompts, generate_video_prompts, generate_prompts

class TestPromptGeneration(unittest.TestCase):
    @patch('openai.ChatCompletion.create')
    def test_generate_image_prompts(self, mock_create):
        # Mock the API response as per expected format
        mock_create.return_value = {
            "choices": [{"message": {"content": "**1. Prompt Title**: Description of the first prompt\n\n**2. Prompt Title**: Description of the second prompt"}}]
        }
        script = "Here is a simple story"
        num_image_prompts = 2
        result = generate_image_prompts(script, num_image_prompts)
        self.assertIn('Description of the first prompt', result['choices'][0]['message']['content'])

    @patch('openai.ChatCompletion.create')
    def test_generate_video_prompts(self, mock_create):
        # Ensure the correct format is returned by the mock
        mock_create.return_value = {
            "choices": [{"message": {"content": "Here is a shorter prompt suitable for video"}}]
        }
        image_prompt = "Detailed image prompt"
        script = "Continuation of the story"
        result = generate_video_prompts(image_prompt, script)
        self.assertEqual(result, "Here is a shorter prompt suitable for video")

    @patch('generate_prompts.generate_image_prompts')
    @patch('generate_prompts.generate_video_prompts')
    def test_generate_prompts(self, mock_video, mock_image):
        # Adjust mock returns to match the actual expected format from the mocked functions
        mock_image.return_value = {'choices': [{'message': {'content': "**1. Prompt Title**: Description for image\n\n**2. Prompt Title**: Another description"}}]}
        mock_video.return_value = "Shorter video prompt description"
        script = "Story for testing"
        num_image_prompts = 2
        result = generate_prompts(script, num_image_prompts)
        self.assertIn("Description for image", result[0])
        self.assertIn("Shorter video prompt description", result[1])

if __name__ == '__main__':
    unittest.main()