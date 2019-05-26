import logging
import sys
from rekognition_ops import RekognitionOps
from polly_ops import PollyOps
from camera_ops import CameraOps
from speaker_ops import SpeakerOps
from greeting_ops import GreetingOps

# Set logger
logger = logging.getLogger(__name__)

class Decider(CameraOps, RekognitionOps,PollyOps,SpeakerOps,GreetingOps):
    """
    Decider: This module is responsible for calling all other modules and acts
        as the orchestrator. Upon detection it will take a picture, find out
        who it is, gather a greeting, turn that greeting into a speech stream,
        and say the greeting
    """
    def __init__(self):
        RekognitionOps.__init__(self)
        CameraOps.__init__(self)
        PollyOps.__init__(self)
        SpeakerOps.__init__(self)
        GreetingOps.__init__(self)

    def orchestrate(self):
        # Call the camera module to take a picture
        faceFrame = self.detect_face()
        # Find the name of the person in the picture
        personName = self.search_faces_by_image(faceFrame)
        if not personName: return None
        logger.info('Name of person identified={}'.format(personName))
        # Look up a custom greeting for the guest
        greeting = self.get_greeting(personName)
        # Turn the greeting into a speech stream
        greetingAudio = self.synthesize_speech(text=greeting)
        # Say greeting to user
        self.play_audio_stream(greetingAudio['AudioStream'])
        return personName



if __name__=='__main__':
    # Set default logging level
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')
    obj = Decider()
    while True: obj.orchestrate()

