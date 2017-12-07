import boto3

client = boto3.client('rekognition', region_name='us-east-1')

photo_path = raw_input("Photo Path in S3\n")

s3_face = {
    'S3Object': {
        'Bucket': 'deeplens-stuff',
        'Name': photo_path
    }
}

collections = client.list_collections()
if not collections['CollectionIds'].__contains__("carlos_test"):
    print("Creating Collection")
    create_resp = client.create_collection(CollectionId="carlos_test")
    print(create_resp)

res = client.search_faces_by_image(CollectionId="carlos_test", Image=s3_face, MaxFaces=5, FaceMatchThreshold=70.0)

if res['SearchedFaceConfidence'] < 90:
    print("Warning! Not sure there is even a face")

location = res['SearchedFaceBoundingBox']
face_matches = res['FaceMatches']
if len(face_matches) < 1:
    print("No matches found")

for match in face_matches:
    similarity = match['Similarity']
    amazon_id = match['Face']['ImageId']
    external_id = match['Face']['ExternalImageId']

    print("External Id: " + external_id)
    print("Amazon Id: " + amazon_id)
    print(str.format("Similarity: {:.0f}%", similarity))

