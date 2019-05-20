import io
import pygame

class SpeakerOps:
    """
    SpeakerOps: This module is responsible for playing the greeting stream
    """
    def __init__(self):
        # PyGame initialization - upon module loading
        pygame.init() 
        pygame.mixer.init() 

    # Convert boto3 audio stream to Bytes stream
    # for compatibility with pygame
    def play_audio_stream(self, audioStream):
        audio = io.BytesIO(audioStream.read())
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        #pygame.mixer.quit()
        #pygame.quit()
