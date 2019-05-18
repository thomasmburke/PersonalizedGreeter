import logging
import io
import sys
from rekognition_ops import RekognitionOps
from polly_ops import PollyOps
from camera_ops import CameraOps
from speaker_ops import SpeakerOps

class Decider(CameraOps, RekognitionOps,PollyOps,SpeakerOps):
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

    def orchestrate(self):
        # Call the camera module to take a picture
        photoStream = self.detect_face()
        # Find the name of the person in the picture
        personName = self.search_faces_by_image(photoStream)
        logger.info('Name of person identified={}'.format(personName))
        # Look up a custom greeting for the user
        # Turn the greeting into a speech stream
        greetingStream = self.synthesize_speech(text=personName)
        # Say greeting to user
        self.play_audio_stream(greetingStream['AudioStream'])
        return self.orchestrate()



if __name__=='__main__':
    # Set default logging level
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')
    obj = Decider()
    print(obj.orchestrate())

