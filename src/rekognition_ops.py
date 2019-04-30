import boto3
from botocore.exceptions import ClientError
import json
import logging

# Set default logging level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        """
        # Add face via s3 file
        response = client.index_faces(
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
        response = client.index_faces(
        CollectionId=self.collectionId, # Collection to add the face to
        MaxFaces=1, # Number of faces to index from the given image
        ExternalImageId=photoName,
        Image=photoData
        )



if __name__=='__main__':
    print(RekognitionOps().describe_collection())
