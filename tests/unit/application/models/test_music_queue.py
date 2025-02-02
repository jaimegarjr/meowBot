from collections import deque
from meowbot.application.models.music_queue import MusicQueue


def test_music_queue_initialization():
    """Test the initialization of MusicQueue."""
    music_queue = MusicQueue()

    assert music_queue is not None
    assert music_queue.queue == deque()
    assert music_queue.current_song is None


def test_add_to_queue():
    """Test the add_to_queue method."""
    music_queue = MusicQueue()
    song = "https://www.youtube.com/watch?v=6n3pFFPSlW4"
    result = music_queue.add_to_queue(song)

    assert result is not None
    assert result == 1
    assert music_queue.queue == deque([song])


def test_remove_from_queue():
    """Test the remove_from_queue method."""
    music_queue = MusicQueue()
    song = "https://www.youtube.com/watch?v=6n3pFFPSlW4"
    music_queue.add_to_queue(song)
    result = music_queue.remove_from_queue()

    assert result is not None
    assert result == song
    assert music_queue.queue == deque()


def test_remove_from_queue_empty_queue():
    """Test remove_from_queue when queue is empty."""
    music_queue = MusicQueue()
    result = music_queue.remove_from_queue()

    assert result is None
    assert music_queue.queue == deque()


def test_is_empty():
    """Test the is_empty method."""
    music_queue = MusicQueue()
    result = music_queue.is_empty()

    assert result is not None
    assert result is True


def test_clear():
    """Test the clear method."""
    music_queue = MusicQueue()
    song = "https://www.youtube.com/watch?v=6n3pFFPSlW4"
    music_queue.add_to_queue(song)
    music_queue.clear()

    assert music_queue.queue == deque()
    assert music_queue.current_song is None
