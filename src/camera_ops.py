from picamera import PiCamera
from time import sleep
from imutils.video import VideoStream, FPS
import cv2
import imutils
import logging

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
        self.fps = FPS().start()
        logger.info('Waiting for camera to warmup...')
        sleep(2)

    def detect_face(self):
        detector = cv2.CascadeClassifier('../HaarCascade/haarcascade_frontalface_default.xml')
        logger.info('Starting video stream...')
        #vs = VideoStream(usePiCamera=True).start()
        # Start frame per second counter
        #fps = FPS().start()
        
        while True:
            frame = self.vs.read()
            frame = imutils.resize(frame, width=500)
            # Convert the input frame from BGR to grayscale - purpose: to detect faces
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces from grayscale frame
            faceRects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(55,55))
            #print(faceRects)
            logger.info('face localized at the following location {}'.format(faceRects))
            # Check if there are any faces in the current frame
            if len(faceRects):
                # Show photo if pi has display
                #cv2.imshow("Frame", frame)
                #key = cv2.waitKey(1) & 0xFF
                success, encodedImage = cv2.imencode(self.fileFormat, frame)
                return encodedImage.tobytes()
