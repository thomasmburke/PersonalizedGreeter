import boto3
from botocore.exceptions import ClientError
import logging
import os

# Set logger
logger = logging.getLogger(__name__)


class RekognitionOps:
    """
    RekognitionOps: Module responsible for all AWS Rekognition operations
    Description: Used to create, delete, describe, search rekognition collections.
        Also able to add faces, delete faces, list faces in a collection.
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
            logger.info('Retreiving image from: {0}'.format(os.path.join(bucket, photoName)))
            # Add face via s3 file
            # response = self.rekognitionClient.index_faces(
            #     CollectionId=self.collectionId, # Collection to add the face to
            #     MaxFaces=1, # Number of faces to index from the given image
            #     ExternalImageId=photoName,
            #     Image={
            #         'S3Object': {
            #             'Bucket': bucket,
            #             'Name': photoName,
            #         }
            #     }
            # )
            # Add face via bytes object
            response = self.rekognitionClient.index_faces(
                CollectionId=self.collectionId,  # Collection to add the face to
                MaxFaces=1,  # Number of faces to index from the given image
                ExternalImageId=photoName,
                Image={'Bytes': photoData}
            )
            logger.info('Status code: {0}'.format(str(response['ResponseMetadata']['HTTPStatusCode'])))
            # If no faces were added ensure that this is logged
            if not response['FaceRecords']:
                logger.warning('No Face was added from image {0}'.format(photoName))
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.error('The collection {0} was not found'.format(self.collectionId))
            else:
                logger.error('Error other than Not Found occurred: {0}'.format(e.response['Error']['Message']))
            logger.error('Operation returned status code: {}'.format(e.response['ResponseMetadata']['HTTPStatusCode']))
            return e.response

    def delete_faces_from_collection(self, faceIds):
        """
        Summary: Deletes faces from a collection. You specify a collection ID and an array of face IDs to remove from the collection.
            This operation requires permissions to perform the rekognition:DeleteFaces action.
        Params: faceIds (LIST) - An array of face IDs to delete.
        Return: response (DICT) - response JSON from rekognition API call
        """
        if not faceIds:
            return None
        try:
            logging.info('Deleting the following faces from {0}\n{1}'.format(self.collectionId, faceIds))
            response = self.rekognitionClient.delete_faces(CollectionId=self.collectionId,
                                                           FaceIds=faceIds)
            logger.info('Status code: {0}'.format(str(response['ResponseMetadata']['HTTPStatusCode'])))
            logger.info('Faces Deleted: {0}'.format(response['DeletedFaces']))
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.error('The collection {0} was not found'.format(self.collectionId))
            else:
                logger.error('Error other than Not Found occurred: {0}'.format(e.response['Error']['Message']))
            logger.error('Operation returned status code: {}'.format(e.response['ResponseMetadata']['HTTPStatusCode']))
            return e.response

    def list_faces(self):
        """
        Summary: List faces in a Rekognition Collection.
            This operation requires permissions to perform the rekognition:ListFaces action
        Return: response (DICT) - response JSON from rekognition API call
        """
        try:
            logger.info('Listing faces in collection: {0}'.format(self.collectionId))
            response = self.rekognitionClient.list_faces(CollectionId=self.collectionId)
            logger.info('Status code: {0}'.format(str(response['ResponseMetadata']['HTTPStatusCode'])))
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.error('The collection {0} was not found'.format(self.collectionId))
            else:
                logger.error('Error other than Not Found occurred: {0}'.format(e.response['Error']['Message']))
            logger.error('Operation returned status code: {}'.format(e.response['ResponseMetadata']['HTTPStatusCode']))
            return e.response

    def search_faces_by_image(self, bucket, photoName, photoData):
        """
        Summary: For a given input image, first detects the largest face in the image, and then searches the specified collection for matching faces.
            The operation compares the features of the input face with faces in the specified collection.
            This operation requires permissions to perform the rekognition:SearchFacesByImage action.
        Params: bucket (STRING) - name of s3 bucket
            photoName (STRING) - s3 object key name
            photoData (Bytes) - Blob of image bytes up to 5 MBs.
        Return: response['FaceMatches'][0]['Face']['ExternalImageId'] (STRING) - name of the face it matches.
            if not faces match it returns None
        Notes: response (DICT) - The response returns an array of faces that match, ordered by similarity score with the highest similarity first.
            More specifically, it is an array of metadata for each face match found. Along with the metadata, the response
            also includes a similarity indicating how similar the face is to the input face. In the response,
            the operation also returns the bounding box (and a confidence level that the bounding box contains a face) of
            the face that Amazon Rekognition used for the input image.
        """
        try:
            logger.info('Dectecting faces in image and adding them to Collection: {0}'.format(self.collectionId))
            logger.info('Retreiving image from: {0}'.format(os.path.join(bucket, photoName)))
            # Add face via s3 file
            # response = self.rekognitionClient.search_faces_by_image(
            #     CollectionId=self.collectionId,  # Collection to add the face to
            #     MaxFaces=1,  # Number of faces to index from the given image
            #     FaceMatchThreshold=70,  # Need 70% confidence in the match
            #     Image={
            #         'S3Object': {
            #             'Bucket': bucket,
            #             'Name': photoName,
            #         }
            #     }
            # )
            # Add face via bytes object
            response = self.rekognitionClient.search_faces_by_image(
                CollectionId=self.collectionId,  # Collection to add the face to
                MaxFaces=1,  # Number of faces to index from the given image
                FaceMatchThreshold=70,  # Need 70% confidence in the match
                Image={'Bytes': photoData}
            )
            logger.info('Status code: {0}'.format(str(response['ResponseMetadata']['HTTPStatusCode'])))
            if not response['FaceMatches']:
                return None
            return response['FaceMatches'][0]['Face']['ExternalImageId']
        except ClientError as e:
            logger.error(e.response)
            return None

    def get_all_face_ids(self):
        """
        Summary: Gets a list of all faces in collection and returns a list of faceIds
        Return: faceIds (LIST) - A list of all face ids in a collection
        """
        faceResponse = self.list_faces()
        faceIds = []
        for face in faceResponse['Faces']:
            faceIds.append(face.get('FaceId'))
        return faceIds
