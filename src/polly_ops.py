import boto3
from botocore.exceptions import ClientError
import logging

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
                VoiceId='Joanna',
                TextType='ssml')
            return response
        except ClientError as e:
            return e.response


if __name__ == '__main__':
    from speaker_ops import SpeakerOps
    response = PollyOps().synthesize_speech(text="""<speak>Want to hear Victoria's Secret? <break time='1s'/><amazon:effect name='whispered'>She has a crush on {}</amazon:effect></speak>""".format('Thomas Burke'))
    SpeakerOps().play_audio_stream(response['AudioStream'])
