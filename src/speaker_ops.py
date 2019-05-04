import io
import pygame

class SpeakerOps:
    """
    SpeakerOps: This module is responsible for playing the greeting stream
    """
    def __init__(self):
        pass

    # Convert boto3 audio stream to Bytes stream
    # for compatibility with pygame
    def play_audio_stream(audioStream):
        # PyGame initialization - upon module loading
        pygame.init() # may want to initialize once in the detector
        pygame.mixer.init() # may want to initialize once in the detector
        audio = io.BytesIO(audioStream.read())
        play_audio(audio)
        pygame.mixer.quit()
        pygame.quit()

    # Here we play the audio stream
    def play_audio(audio):
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
