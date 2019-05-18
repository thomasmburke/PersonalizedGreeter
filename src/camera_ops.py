from picamera import PiCamera
from time import sleep
import io
from imutils.video import VideoStream, FPS
import cv2
import imutils

class CameraOps:
    """
    CameraOps: Responsible for taking a picture of the person and streaming
        the photo back to Decider
    """
    def __init__(self):
        #self.camera = PiCamera()
        self.photoStream = io.BytesIO()
        self.fileFormat = 'jpeg'

    #def take_picture(self):
    #    self.camera.start_preview()
    #    sleep(1)
    #    self.camera.capture(self.photoStream, format=self.fileFormat)
    #    self.camera.stop_preview()
    #    # Rewind the stream to the beginning so we can read its content
    #    self.photoStream.seek(0)
    #    return self.photoStream

    def detect_face(self):
        detector = cv2.CascadeClassifier('/home/pi/Downloads/pi-face-recognition/haarcascade_frontalface_default.xml')
        print('Starting video stream...')
        vs = VideoStream(usePiCamera=True).start()
        # Waiting for camera to warmup
        print('Waiting for camera to warmup...')
        sleep(2)
        # Start frame per second counter
        fps = FPS().start()
        
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=500)
        
            # Convert the input frame from BGR to grayscale - purpose: to detect faces
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces from grayscale frame
            rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(55,55))
            print(rects)
            if len(rects):
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF
                success, encodedImage = cv2.imencode('.jpg', frame)
                return encodedImage.tobytes()
