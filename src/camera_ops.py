from picamera import PiCamera
from time import sleep
import io

class CameraOps:
    """
    CameraOps: Responsible for taking a picture of the person and streaming
        the photo back to Decider
    """
    def __init__(self):
        self.camera = PiCamera()
        self.photoStream = io.BytesIO()
        self.fileFormat = 'jpeg'

    def take_picture(self):
        self.camera.start_preview()
        sleep(5)
        self.camera.capture(self.photoStream, format=self.fileFormat)
        self.camera.stop_preview()
        # Rewind the stream to the beginning so we can read its content
        self.photoStream.seek(0)
        photoStream.close()

"""
camera = PiCamera()
photoStream = io.BytesIO()
camera.start_preview()
sleep(5)
camera.capture(photoStream, format='jpeg')
camera.stop_preview()
# "Rewind" the stream to the beginning so we can read its content
photoStream.seek(0)
"""
