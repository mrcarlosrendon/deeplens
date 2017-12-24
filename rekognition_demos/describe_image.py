import math
import boto3
import sys
from PIL import Image

COLLECTION_ID = "carlos_test"
MATCH_THRESHOLD = 70.0
client = boto3.client('rekognition', region_name='us-east-1')

def crop_n_save(fn, out_fn, bounds):
    im = Image.open(fn)
    #print(im.size)
    #print(bounds)
    (width, height) = im.size
    left = bounds['Left']*width
    top = bounds['Top']*height
    box = (left, top, left + (bounds['Width']*width), top + (bounds['Height']*height))
    #print(box)
    im.crop(box).save(out_fn)

def value_if_confidence(value, confidence):
    if value['Confidence'] > confidence:
        return value['Value']
    
def describe_face(face):
    age = face['AgeRange']
    age_str = str(age['Low']) + "-" + str(age['High'])
    emotions = face['Emotions']
    emotions_lst = []
    for emotion in emotions:
        if emotion['Confidence'] > 90:
            emotions_lst.append(emotion['Type'])
    print("Face Info")
    print("Age: " + age_str  + " years old")
    print("Emotions: " + str(emotions_lst))
    items = ['Gender', 'EyesOpen', 'MouthOpen', 'Smile', 'Eyeglasses', 'Sunglasses', 'Beard', 'Mustache']
    for item in items:
        print(item + ": " + str(value_if_confidence(face[item], 90.0)))
    print("")
    
def identify_face(fn):
    with open(fn, 'rb') as face:
        res = client.search_faces_by_image(CollectionId=COLLECTION_ID, Image={"Bytes": face.read()}, MaxFaces=5, FaceMatchThreshold=MATCH_THRESHOLD)
    
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
            break

def main():
    pic_file = sys.argv[1]
    print("processing: " + pic_file)
    with open(pic_file, 'rb') as test:        
        res = client.detect_faces(Image={"Bytes": test.read()}, Attributes=['ALL'])
        face_list = res['FaceDetails']
        for num, face in enumerate(face_list):
            bounds = face['BoundingBox']
            face_file = "face_" + str(num) + ".jpg"
            print("processing: " + face_file)
            crop_n_save(pic_file, face_file, bounds)
            identify_face(face_file)
            describe_face(face)

main()
    

