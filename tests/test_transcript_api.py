import pytest
def test_youtube_transcript_api_call_shape():
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except Exception:
        pytest.skip("youtube_transcript_api not installed")
    assert hasattr(YouTubeTranscriptApi, "fetch")
    assert hasattr(YouTubeTranscriptApi, "list")
