import boto3
from botocore.exceptions import ClientError
import json
import logging
import os

# Set default logging level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#TODO: get function name in logger


class RekognitionOps:
    """
    Rekognition: Module responsible for all AWS Rekognition operations
    Description: Used to create and delete rekognition collections
    Attributes: collectionId (STRING) - Used to indentify the collection to
            interact with
        rekognitionClient (boto3.client) - Used to interact directly with AWS
            rekognition
    """
    def __init__(self):
        self.collectionId = 'FriendsCollection'
        self.rekognitionClient = boto3.client('rekognition')

    def create_collection(self):
        """
        Summary: Create a Rekognition Collection
        Return: response (DICT) - response JSON from rekognition API call
        """
        try:
            logger.info('Creating collection with collection ID: {0}'.format(self.collectionId))
            response = self.rekognitionClient.create_collection(CollectionId=self.collectionId)
            logger.info('Collection ARN: {0}'.format(response['CollectionArn']))
            logger.info('Status code: {0}'.format(str(response['StatusCode'])))
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                logger.error('The collection {0} already exists'.format(self.collectionId))
            else:
                logger.error('Error other than Already Exists occurred: {0}'.format(e.response['Error']['Message']))
            logger.error('Operation returned status code: {}'.format(e.response['ResponseMetadata']['HTTPStatusCode']))
            return e.response

    def delete_collection(self):
        """
        Summary: Delete a Rekognition Collection
        Return: response (DICT) - response JSON from rekognition API call
        """
        try:
            logger.info('Deleting collection with collection ID: {0}'.format(self.collectionId))
            response = self.rekognitionClient.delete_collection(CollectionId=self.collectionId)
            logger.info('Status code: {0}'.format(str(response['StatusCode'])))
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.error('The collection {0} was not found'.format(self.collectionId))
            else:
                logger.error('Error other than Not Found occurred: {0}'.format(e.response['Error']['Message']))
            logger.error('Operation returned status code: {}'.format(e.response['ResponseMetadata']['HTTPStatusCode']))
            return e.response

    def describe_collection(self):
        """
        Summary: Describe a Rekognition Collection
        Return: response (DICT) - response JSON from rekognition API call
        """
        try:
            logger.info('Describing collection with collection ID: {0}'.format(self.collectionId))
            response = self.rekognitionClient.describe_collection(CollectionId=self.collectionId)
            logger.info('Status code: {0}'.format(str(response['ResponseMetadata']['HTTPStatusCode'])))
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.error('The collection {0} was not found'.format(self.collectionId))
            else:
                logger.error('Error other than Not Found occurred: {0}'.format(e.response['Error']['Message']))
            logger.error('Operation returned status code: {}'.format(e.response['ResponseMetadata']['HTTPStatusCode']))
            return e.response

    def add_face_to_collection(self, bucket, photoName, photoData):
        """
        Summary: This operation detects faces in an image and adds them to the specified Rekognition collection.
            The face's feature vectors are pulled out from the the image and stored in the collection, not
            the image itself
        Params: bucket (STRING) - name of s3 bucket
            photoName (STRING) - s3 object key name
            photoData (Bytes) - Blob of image bytes up to 5 MBs.
        Return response (DICT) - response JSON from rekognition API call
        """
        try:
            logger.info('Dectecting faces in image and adding them to Collection: {0}'.format(self.collectionId))
            logger.info('Retreiving image from: {0}'.format(os.path.join(bucket,photoName)))
            # Add face via s3 file
            response = self.rekognitionClient.index_faces(
                CollectionId=self.collectionId, # Collection to add the face to
                MaxFaces=1, # Number of faces to index from the given image
                ExternalImageId=photoName,
                Image={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': photoName,
                    }
                }
            )
            # Add face via bytes object
            response = self.rekognitionClient.index_faces(
                CollectionId=self.collectionId, # Collection to add the face to
                MaxFaces=1, # Number of faces to index from the given image
                ExternalImageId=photoName,
                Image=photoData
            )
            #TODO: log the status code of the response
            return response
        except ClientError as e:
            #TODO: catch common exception
            #TODO: catch all other exceptions
            #TODO: log the status code and error
            return e.response

    def delete_faces_from_collection(self,faceIds):
        """
        Summary: Deletes faces from a collection. You specify a collection ID and an array of face IDs to remove from the collection.
            This operation requires permissions to perform the rekognition:DeleteFaces action.
        Params: faceIds (LIST) - An array of face IDs to delete.
        Return: response (DICT) - response JSON from rekognition API call
        """
        try:
            logging.info('Deleting the following faces from {0}\n{1}'.format(self.collectionId, faceIds))
            response = self.rekognitionClient.delete_faces(CollectionId=self.collectionId,
                    FaceIds=faceIds)
            #TODO print out HTTP status code
            return response
        except ClientError as e:
            #TODO: catch common exception
            #TODO: catch all other exceptions
            #TODO: log the status code and error
            return e.response


if __name__=='__main__':
    print(RekognitionOps().describe_collection())
