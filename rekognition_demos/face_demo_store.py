import boto3

client = boto3.client('rekognition', region_name='us-east-1')

photo_path = raw_input("Photo Path in S3\n")
face_name = raw_input("Name of face in photo\n")

s3_face = {
    'S3Object':
    {
        'Bucket': 'deeplens-stuff',
        'Name': photo_path
    }
}

collections = client.list_collections()
if not collections['CollectionIds'].__contains__("carlos_test"):
    print("Creating Collection")
    create_resp = client.create_collection(CollectionId="carlos_test")
    print(create_resp)

res = client.index_faces(CollectionId="carlos_test", Image=s3_face, ExternalImageId=face_name, DetectionAttributes=[])

print(res)
