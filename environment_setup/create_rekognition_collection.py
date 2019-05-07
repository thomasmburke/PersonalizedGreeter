import logging
import sys
import os
sys.path.insert(0, '../src')
from rekognition_ops import RekognitionOps

if __name__ == '__main__':
    # Set default logging level
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')
    RekognitionOps().create_collection()
    # All faces in the dataset are stored locally, so I am iterating through all of them
    faceImages = os.listdir('/Users/tburke/Desktop/facebook_pics/')
    for faceImage in faceImages:
        with open('/Users/tburke/Desktop/facebook_pics/{}'.format(faceImage), 'rb') as myFile:
            encoded_string = myFile.read()
            RekognitionOps().add_face_to_collection(os.path.splitext(faceImage)[0], encoded_string)
    """
    # To clear collection of all faces
    faceIds = RekognitionOps().get_all_face_ids()
    print(RekognitionOps().delete_faces_from_collection(faceIds))
    """
