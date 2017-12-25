import awscam
import cv2
from timeit import default_timer as timer

import describe_image

print("Loading...")
load_start = timer()
modelPath = "/opt/awscam/artifacts/mxnet_deploy_ssd_FP16_FUSED.xml"
modelType = "ssd"
input_width = 300
input_height = 300
prob_thresh = 0.25

scale = 1.0/2

# Load model to GPU (use {"GPU": 0} for CPU)
mcfg = {"GPU": 1}
model = awscam.Model(modelPath, mcfg)
ret, frame = awscam.getLastFrame() 
if ret == False:
    raise Exception("Failed to get frame from the stream")
ret, frame = awscam.getLastFrame()
            
yscale = float((frame.shape[0]/2.)/input_height)
xscale = float((frame.shape[1]/2.)/input_width)

print("height: " + str(frame.shape[0]))
print("width: " + str(frame.shape[1]))
print("yscale: " + str(yscale))
print("xscale: " + str(xscale))

print("Loading Time: " + str(timer() - load_start))

while True:
    start = timer()
    ret = False    
    while not ret:
        ret, img = awscam.getLastFrame()
    get_frames = timer()
    print("Get Frames Time: " + str(get_frames - start))
    # Scale for SPEED
    scaled = cv2.resize(img, None, fx=scale, fy=scale)
    scale_down = timer()
    print("Scale Down Time: " + str(scale_down - get_frames))
    model_frame = cv2.resize(scaled, (input_width, input_height))
    infer = model.doInference(model_frame)
    face_list = model.parseResult(modelType, infer)['ssd']
    detect_faces = timer()
    print("Detect Faces Time: " + str(detect_faces - scale_down))    
    for num, face in enumerate(face_list):
        if face['prob'] < prob_thresh:
            break
        #print("Inference Size: " + str((input_width, input_height)))
        #print("Scaled Size: " + str(scaled.shape))
        #print("(xmin, xmax) - " + str(face['xmin']) + " " + str(face['xmax']))
        #print("xscale: " + str(xscale))
        #print("mult: " + str( int( xscale * face['xmin'])))
        xmin = int( xscale * face['xmin'] )
        ##+ int((face['xmin'] - input_width/2) + input_width/2)
        ymin = int( yscale * face['ymin'] )
        xmax = int( xscale * face['xmax'] )
        ##+ int((face['xmax'] - input_width/2) + input_width/2)
        ymax = int( yscale * face['ymax'] )
        cv2.rectangle(scaled, (xmin, ymin), (xmax, ymax), (255, 165, 20), 4)
        bounds = (xmin, xmax, ymin, ymax)
        print("analyzing: face " + str(num))
        face_name = describe_image.identify_face(scaled, bounds)
        identify_face = timer()
        print("Identify Time: " + str(identify_face - detect_faces))
        print(face_name)
        describe_image.label_face(scaled, bounds, face_name)
        #describe_image.describe_face(scaled, bounds, face)
    cv2.imshow('Result', scaled)
    cv2.waitKey(100)
    end = timer()
    print("Frame Time: " + str(end - start))
    print("")
