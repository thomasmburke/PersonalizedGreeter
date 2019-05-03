import logging
import sys
sys.path.insert(0, '../src')
from rekognition_ops import RekognitionOps

if __name__ == '__main__':
    # Set default logging level
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')
    with open('C:/Users/thomas.burke/OneDrive - Accenture/Desktop/ThomasBurke.PNG', 'rb') as myFile:
        # with open('C:/Users/thomas.burke/OneDrive - Accenture/Desktop/jeff.jpg', 'rb') as myFile:
        encoded_string = myFile.read()
    # with open('/Users/tburke/Desktop/ThomasBurke.png', 'rb') as myFile:
        #encoded_string = base64.b64encode(myFile.read())
        #encoded_string = myFile.read()
    #print(RekognitionOps().add_face_to_collection('bucket', 'ThomasBurke', encoded_string))
    # print(RekognitionOps().list_faces())
    print(RekognitionOps().search_faces_by_image('bucket', 'photoName', encoded_string))
