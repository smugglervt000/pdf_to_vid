import unittest
from unittest.mock import patch, MagicMock
import animate_video_clips

class TestAnimateVideoClips(unittest.TestCase):
    @patch('animate_video_clips.requests.get')
    def test_download_pexels_video(self, mock_get):
        """Test the download_pexels_video function to handle API interactions and file writing."""
        # Mock the API response
        mock_get.return_value.ok = True
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'videos': [{'video_files': [{'link': 'http://example.com/video.mp4'}]}]
        }
        mock_get.return_value.content = b'video content'
        
        # Mock open to avoid actual file writing
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            output = animate_video_clips.download_pexels_video('dummy_api_key', 'nature', 'output.mp4', 10)

        self.assertEqual(output, 'output.mp4')
        mock_file.assert_called_with('temp_video.mp4', 'wb')
        mock_get.assert_called()

    @patch('animate_video_clips.VideoFileClip')
    @patch('animate_video_clips.CompositeVideoClip')
    def test_crossfade_videos(self, mock_composite_video_clip, mock_video_clip):
        """Test the crossfade between two video files."""
        animate_video_clips.crossfade_videos('video1.mp4', 'video2.mp4', 3)
        mock_video_clip.assert_called()
        self.assertTrue(mock_composite_video_clip.called)

if __name__ == '__main__':
    unittest.main()