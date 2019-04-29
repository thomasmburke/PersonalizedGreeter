import logging
import sys
sys.path.insert(0, '../src')
from rekognition_ops import RekognitionOps

if __name__ == '__main__':
    # Set default logging level
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    RekognitionOps().create_collection()
