import awscam
import cv2
from timeit import default_timer as timer

import describe_image

while True:
    start = timer()
    for x in range(0, 10):        
        awscam.getLastFrame()
    ret = False    
    while not ret:
        ret, img = awscam.getLastFrame()
    get_frames = timer()
    print("Get Frames Time: " + str(get_frames - start))
    # Scale for SPEED
    scale = 1.0/2
    scaled = cv2.resize(img, None, fx=scale, fy=scale)
    scale_down = timer()
    print("Scale Down Time: " + str(scale_down - get_frames))
    face_list = describe_image.detect_faces(scaled)
    detect_faces = timer()
    print("Detect Faces Time: " + str(detect_faces - scale_down))
    print("Num Faces: " + str(len(face_list)))
    for num, face in enumerate(face_list):
        bounds = describe_image.aws_bounds_to_cv_bounds(scaled, face['BoundingBox'])
        print("analyzing: face " + str(num))
        face_name = describe_image.identify_face(scaled, bounds)
        identify_face = timer()
        print("Identify Time: " + str(identify_face - detect_faces))
        print(face_name)
        describe_image.label_face(scaled, bounds, face_name)
        describe_image.describe_face(scaled, bounds, face)
    cv2.imshow('Result', scaled)
    cv2.waitKey(100)
    end = timer()
    print("Frame Time: " + str(end - start))
    print("")
