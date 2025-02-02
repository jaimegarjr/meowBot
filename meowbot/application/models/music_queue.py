from collections import deque


class MusicQueue:
    def __init__(self):
        self.queue = deque()
        self.current_song = None

    def add_to_queue(self, song):
        self.queue.append(song)
        return len(self.queue)

    def remove_from_queue(self):
        if self.queue:
            return self.queue.popleft()

        self.current_song = None
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def clear(self):
        self.queue.clear()
        self.current_song = None
