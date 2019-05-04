import logging
import io
from rekognition_ops import RekognitionOps
from polly_ops import PollyOps
from camera_ops import CameraOps
#from speaker_ops import SpeakerOps

class Decider(CameraOps, RekognitionOps):
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
        photoStream = self.take_picture()
        # Find the name of the person in the picture
        personName = self.search_faces_by_image('bucket','photoName', photoStream.getvalue())
        photoStream.close()
        return personName
        # Look up a custom greeting for the user
        # Turn the greeting into a speech stream
        # Say greeting to user


if __name__=='__main__':
    obj = Decider()
    print(obj.orchestrate())

