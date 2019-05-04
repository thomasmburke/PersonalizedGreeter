import boto3
from botocore.exceptions import ClientError
import logging
import io
import pygame

# Set logger
logger = logging.getLogger(__name__)


class PollyOps:
    """
    PollyOps: Module responsible for all AWS Polly operations
    Description: Used to convert text to speech when a user arrives
    Attributes: pollyClient (boto3.client) - Used to interact directly with AWS polly
    """

    def __init__(self):
        self.pollyClient = boto3.client('polly')

    def synthesize_speech(self, text):
        """
        Summary: Convert text or SSML to speech
        """
        try:
            logger.info('Calling Polly to do TTS...')
            response = self.pollyClient.synthesize_speech(
                OutputFormat='ogg_vorbis',
                Text=text,
                VoiceId='Joanna')
            return response
        except ClientError as e:
            return e.response


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    response = PollyOps().synthesize_speech(text='All Gaul is divided into three parts')
    print(response)
    audio = io.BytesIO(response['AudioStream'].read())
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
