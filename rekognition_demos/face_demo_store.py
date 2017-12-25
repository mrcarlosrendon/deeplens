import sys
import boto3

COLLECTION_ID = "carlos_test"

client = boto3.client('rekognition', region_name='us-west-2')

if (not len(sys.argv) == 3):
    print("Usage face_demo_store.py [image file] [face name]")
    exit(1)

photo_path = sys.argv[1]
face_name = sys.argv[2]

collections = client.list_collections()
if not collections['CollectionIds'].__contains__(COLLECTION_ID):
    print("Creating Collection")
    create_resp = client.create_collection(CollectionId=COLLECTION_ID)
    print(create_resp)

with open(photo_path, 'rb') as face:
    res = client.index_faces(CollectionId=COLLECTION_ID, Image={"Bytes": face.read()}, ExternalImageId=face_name, DetectionAttributes=[])
    print(res)
