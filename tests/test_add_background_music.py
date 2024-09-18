import unittest
from unittest.mock import patch, MagicMock
import background_music

class TestBackgroundMusic(unittest.TestCase):
    @patch('background_music.VideoFileClip')
    @patch('background_music.AudioFileClip')
    @patch('background_music.concatenate_audioclips')
    @patch('background_music.CompositeAudioClip')
    @patch('background_music.os.rename')
    def test_add_background_music(self, mock_rename, mock_composite_audio_clip, mock_concatenate_audioclips, mock_audio_file_clip, mock_video_file_clip):
        # Mock setup
        mock_video = mock_video_file_clip.return_value
        mock_video.duration = 120.0
        mock_video.audio = MagicMock()
        mock_video.audio.volumex.return_value = MagicMock()

        mock_audio = mock_audio_file_clip.return_value
        mock_audio.duration = 30.0
        mock_audio.volumex.return_value = mock_audio

        concatenated_mock = MagicMock()
        concatenated_mock.subclip.return_value = MagicMock()
        mock_concatenate_audioclips.return_value = concatenated_mock

        apiroot = 'api/outputs/'
        root = '/path/to/root'

        # Execute function
        background_music.add_background_music(1, 'video.mp4', apiroot, root)

        # Assertions
        mock_audio_file_clip.assert_called_once_with(apiroot + 'background_music_subtle.mp3')
        mock_audio.volumex.assert_called_once_with(0.1)
        mock_rename.assert_called_once_with(root + "/public/final_merged_video.mp4", root + "/public/final.mp4")

if __name__ == '__main__':
    unittest.main()