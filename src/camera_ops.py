from picamera import PiCamera
from time import sleep
from imutils.video import VideoStream, FPS
import cv2
import imutils
import logging
import os

# Set logger
logger = logging.getLogger(__name__)

class CameraOps:
    """
    CameraOps: Responsible for taking a picture of the person and streaming
        the photo back to Decider
    """
    def __init__(self):
        self.fileFormat = '.jpg'
        self.vs = VideoStream(usePiCamera=True).start()
        # Start frame per second counter
        self.fps = FPS().start()
        logger.info('Waiting for camera to warmup...')
        sleep(2)

    def detect_face(self):
        haarCascadePath = os.path.dirname(__file__) + '/../HaarCascade/haarcascade_frontalface_default.xml'
        logger.info('haar cascade path: {}'.format(haarCascadePath))
        detector = cv2.CascadeClassifier(haarCascadePath)
        logger.info('Resuming video stream...')
        # Setting up frame detection counter to raise the threshold for a face match
        frameDetectCnt = 0
        logger.info('initializing frame detection count to 0')
        
        while True:
            frame = self.vs.read()
            frame = imutils.resize(frame, width=500)
            # Convert the input frame from BGR to grayscale - purpose: to detect faces
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces from grayscale frame
            faceRects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7, minSize=(55,55))
            # Check if there are any faces in the current frame
            if len(faceRects):
                frameDetectCnt += 1
                logger.info('frame detection count={}'.format(frameDetectCnt))
                if frameDetectCnt >= 10:
                    logger.info('face localized at the following location {}'.format(faceRects))
                    # Show photo if pi has display
                    #cv2.imshow("Frame", frame)
                    #key = cv2.waitKey(1) & 0xFF
                    success, encodedImage = cv2.imencode(self.fileFormat, frame)
                    return encodedImage.tobytes()
            else: frameDetectCnt = 0
