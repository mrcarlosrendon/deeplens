import math
import sys
import boto3
import cv2
import numpy

OVERLAY_COLOR = (255, 165, 20)
COLLECTION_ID = "carlos_test"
MATCH_THRESHOLD = 70.0
client = boto3.client('rekognition', region_name='us-east-1')

def get_scaled_bounds(img, bounds):
    (height, width, channels) = img.shape
    #print(bounds)
    #print(width, height)
    left = int(bounds['Left']*width)
    top = int(bounds['Top']*height)
    right = int(left + (bounds['Width']*width))
    bottom = int(top + (bounds['Height']*height))
    return (left, right, top, bottom)

def get_display_scale(img):
    (height, width, channels) = img.shape
    scale = 1
    if width > 1980 or height > 1080:
        scale = int(max(width / 1980, height/ 1080))+1
        return 1.0/scale
    return 1

def get_region_bytes(img, bounds):
    (left, right, top, bottom) = get_scaled_bounds(img, bounds)
    img_enc = cv2.imencode(".jpg", img[top:bottom, left:right])
    return numpy.array(img_enc[1]).tostring()

def label_face(img, bounds, name):
    scaled_bounds = get_scaled_bounds(img, bounds)
    #print(scaled_bounds)
    (left, right, top, bottom) = scaled_bounds
    width = 1
    font_size = .5
    if get_display_scale(img) < .6:
        width = 4
        font_size = 2
    cv2.rectangle(img, (left, top), (right, bottom), OVERLAY_COLOR, width)
    cv2.putText(img, name, (left, top-15), cv2.FONT_HERSHEY_SIMPLEX, font_size, OVERLAY_COLOR, width)
    
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
    def value_if_confidence(value, confidence):
        if value['Confidence'] > confidence:
            return value['Value']
    items = ['Gender', 'EyesOpen', 'MouthOpen', 'Smile', 'Eyeglasses', 'Sunglasses', 'Beard', 'Mustache']
    for item in items:
        print(item + ": " + str(value_if_confidence(face[item], 90.0)))
    print("")
    
def identify_face(img, bounds):
    try:
        res = client.search_faces_by_image(CollectionId=COLLECTION_ID, Image={"Bytes": get_region_bytes(img, bounds)}, MaxFaces=5, FaceMatchThreshold=MATCH_THRESHOLD)
    except:
        return "Unidentified"
        
    if res['SearchedFaceConfidence'] < 90:
        print("Warning! Not sure there is even a face")

    location = res['SearchedFaceBoundingBox']
    face_matches = res['FaceMatches']
    if len(face_matches) < 1:
        return "Unidentified"
        
    for match in face_matches:
        similarity = match['Similarity']
        amazon_id = match['Face']['ImageId']
        external_id = match['Face']['ExternalImageId']
        
        print("External Id: " + external_id)
        print("Amazon Id: " + amazon_id)
        print(str.format("Similarity: {:.0f}%", similarity))
        return external_id

def main():
    pic_file = sys.argv[1]
    print("processing: " + pic_file)
    with open(pic_file, 'rb') as test:        
        res = client.detect_faces(Image={"Bytes": test.read()}, Attributes=['ALL'])
        face_list = res['FaceDetails']
        img = cv2.imread(pic_file)
        for num, face in enumerate(face_list):
            bounds = face['BoundingBox']
            print("analyzing: " + "face " + str(num))
            face_name = identify_face(img, bounds)
            label_face(img, bounds, face_name)            
            describe_face(face)
        scale = get_display_scale(img)
        scaled = cv2.resize(img, None, fx=scale, fy=scale)
        cv2.imshow('Result', scaled)
        cv2.waitKey(0)
main()
    

