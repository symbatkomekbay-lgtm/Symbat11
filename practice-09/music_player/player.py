from pathlib import Path
import pygame

class Player:
    def __init__(self):
        folder = Path(__file__).parent / 'music'
        self.tracks = sorted(p for p in folder.rglob('*') if p.suffix.lower() in ('.wav', '.mp3', '.ogg'))
        self.index = 0
        self.playing = False
        self.end_event = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.end_event)

    @property
    def name(self):
        return self.tracks[self.index].stem if self.tracks else 'No tracks found'

    def play(self):
        if self.tracks:
            pygame.mixer.music.load(str(self.tracks[self.index]))
            pygame.mixer.music.play()
            self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        pygame.event.clear(self.end_event)
        self.playing = False

    def change(self, step):
        if self.tracks:
            self.stop()
            self.index = (self.index + step) % len(self.tracks)
            self.play()

    def position(self):
        return max(0, pygame.mixer.music.get_pos()) // 1000 if self.playing else 0
