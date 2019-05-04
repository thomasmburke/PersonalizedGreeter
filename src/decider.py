import logging
from rekognition_ops import RekognitionOps
from polly_ops import PollyOps
from camera_ops import CameraOps
from speaker_ops import SpeakerOps

class Decider:
    """
    Decider: This module is responsible for calling all other modules and acts
        as the orchestrator. Upon detection it will take a picture, find out
        who it is, gather a greeting, turn that greeting into a speech stream,
        and say the greeting
    """
    def __init__(self):
        pass

    def orchestrate(self):
        # Call the camera module to take a picture
        # Find the name of the person in the picture
        # Look up a custom greeting for the user
        # Turn the greeting into a speech stream
        # Say greeting to user


if __name__=='__main__':

