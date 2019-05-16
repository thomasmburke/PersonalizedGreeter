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
    name = 'HannahSugrue'
    with open('/Users/tburke/Desktop/facebook_pics/{}.jpg'.format(name), 'rb') as myFile:
        encoded_string = myFile.read()
        RekognitionOps().add_face_to_collection(name, encoded_string)
    """
    # To clear collection of all faces
    faceIds = RekognitionOps().get_all_face_ids()
    print(RekognitionOps().delete_faces_from_collection(faceIds))
    """
