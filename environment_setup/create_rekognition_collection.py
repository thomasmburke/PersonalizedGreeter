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
    RekognitionOps().create_collection()
