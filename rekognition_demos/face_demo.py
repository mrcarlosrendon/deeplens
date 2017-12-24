import boto3
from PIL import Image

client = boto3.client('rekognition', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

photo_path = raw_input("Photo Path in S3\n")

s3_face = {
    'S3Object': {
        'Bucket': 'deeplens-stuff',
        'Name': photo_path
    }
}

res = client.detect_faces(Image=s3_face, Attributes=['ALL'])

face_list = res['FaceDetails']
print("")
print("Num faces: " + str(len(face_list)))

for face in face_list:
    bounds = face['BoundingBox']
    bounds_str = str.format("{:.0%} from left, {:.0%} from top", bounds['Left'], bounds['Top'])
    age = face['AgeRange']
    age_str = str(age['Low']) + "-" + str(age['High'])
    emotions = face['Emotions']
    emotions_lst = []
    for emotion in emotions:
        if emotion['Confidence'] > 90:
            emotions_lst.append(emotion['Type'])
    gender = face['Gender']
    if gender['Confidence'] > 90:
        gender_str = gender['Value']
    else:
        gender_str = 'Unknown'
    mouth = face['MouthOpen']
    if mouth['Confidence'] > 90:
        mouth_str = 'Open' if mouth['Value'] else 'Closed'
    else:
        mouth_str = 'Unknown'

    print("Face Info")
    print("Upper Left: "+ bounds_str)
    print("Gender: " + gender_str)
    print("Age: " + age_str  + " years old")
    print("Emotions: " + str(emotions_lst))
    print("Mouth: " + mouth_str)
    print("")
