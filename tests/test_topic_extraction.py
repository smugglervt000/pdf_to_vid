import unittest
from unittest.mock import patch, MagicMock
from topic_extraction import text_to_json, topics_from_text  # Adjust the import according to your script's name

class TestTextProcessing(unittest.TestCase):
    def test_text_to_json(self):
        # Sample input text structured with topic numbers
        input_text = "1: Topic One\n- Subtheme A\n- Subtheme B\n2: Topic Two\n- Subtheme C"
        expected_output = '''{
    "Topic One": [
        "Subtheme A",
        "Subtheme B"
    ],
    "Topic Two": [
        "Subtheme C"
    ]
}'''
        result = text_to_json(input_text)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()