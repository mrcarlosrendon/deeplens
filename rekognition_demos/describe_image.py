import math
import sys
import boto3
import cv2
import numpy

OVERLAY_COLOR = (255, 165, 20)
COLLECTION_ID = "carlos_test"
MATCH_THRESHOLD = 70.0
client = boto3.client('rekognition', region_name='us-east-1')

def aws_bounds_to_cv_bounds(img, bounds):
    (height, width, channels) = img.shape
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

def get_display_props(img):
    width = 1
    font_size = .5
    if get_display_scale(img) < .6:
        width = 4
        font_size = 2
    return (width, font_size)

def get_region_bytes(img, bounds):
    (left, right, top, bottom) = bounds
    img_enc = cv2.imencode(".jpg", img[top:bottom, left:right])
    return numpy.array(img_enc[1]).tostring()

def label_face(img, bounds, name):
    (left, right, top, bottom) = bounds
    (width, font_size) = get_display_props(img)
    cv2.rectangle(img, (left, top), (right, bottom), OVERLAY_COLOR, width)
    cv2.putText(img, name, (left, top-15), cv2.FONT_HERSHEY_SIMPLEX, font_size, OVERLAY_COLOR, width)
    
def describe_face(img, bounds, face):
    age = face['AgeRange']
    age_str = str(age['Low']) + "-" + str(age['High'])
    emotions = face['Emotions']
    emotions_lst = []
    for emotion in emotions:
        if emotion['Confidence'] > 90:
            emotions_lst.append(emotion['Type'])

    (width, font_size) = get_display_props(img)
    (left, right, top, bottom) = bounds

    cv2.putText(img, "Age: " + age_str, (left, bottom + int(30*font_size)), cv2.FONT_HERSHEY_SIMPLEX, font_size, OVERLAY_COLOR, width)
    cv2.putText(img, "Emotions: " + str(emotions_lst), (left, bottom + int(2*30*font_size)), cv2.FONT_HERSHEY_SIMPLEX, font_size, OVERLAY_COLOR, width)
    
    def value_if_confidence(value, confidence):
        if value['Confidence'] > confidence:
            return value['Value']
    items = ['Gender', 'EyesOpen', 'MouthOpen', 'Smile', 'Eyeglasses', 'Sunglasses', 'Beard', 'Mustache']
    for (num, item) in enumerate(items):
        cv2.putText(img, item + ": " + str(value_if_confidence(face[item], 90.0)), (left, bottom + int((num+3)*30*font_size)), cv2.FONT_HERSHEY_SIMPLEX, font_size, OVERLAY_COLOR, width)
    
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
        
        #print("External Id: " + external_id)
        #print("Amazon Id: " + amazon_id)
        #print(str.format("Similarity: {:.0f}%", similarity))
        return external_id

def detect_faces(img):
    (height, width, channels) = img.shape
    bites = get_region_bytes(img, (0, width, 0, height))
    res = client.detect_faces(Image={"Bytes": bites}, Attributes=['ALL'])
    return res['FaceDetails']
    
def main():
    pic_file = sys.argv[1]
    print("processing: " + pic_file)
    img = cv2.imread(pic_file)
    face_list = detect_faces(img)
    for num, face in enumerate(face_list):
        bounds = aws_bounds_to_cv_bounds(img, face['BoundingBox'])
        print("analyzing: " + "face " + str(num))
        face_name = identify_face(img, bounds)
        label_face(img, bounds, face_name)            
        describe_face(img, bounds, face)
    scale = get_display_scale(img)
    scaled = cv2.resize(img, None, fx=scale, fy=scale)
    cv2.imshow('Result', scaled)
    cv2.waitKey(0)

if __name__ == "__main__":
   main()

