import unittest
from unittest.mock import patch, MagicMock
from pdf_parser import parse

class TestPDFParsing(unittest.TestCase):
    @patch('fitz.open') 
    def test_parse_pdf(self, mock_open):
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_open.return_value = mock_doc
        mock_doc.__len__.return_value = 1 
        mock_doc.load_page.return_value = mock_page
        mock_page.get_text.return_value = "This is some sample text https://example.com"

        expected_text = "This is some sample text "

        result_text = parse('dummy_path.pdf')
        self.assertEqual(result_text, expected_text)

        mock_doc.close.assert_called_once()

    @patch('fitz.open')  
    def test_empty_pdf(self, mock_open):
        mock_doc = MagicMock()
        mock_open.return_value = mock_doc
        mock_doc.__len__.return_value = 0  

        expected_text = ""

        result_text = parse('dummy_path.pdf')
        self.assertEqual(result_text, expected_text)

        mock_doc.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()