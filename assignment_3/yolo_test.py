import numpy as np
import random
import cv2 as cv
import matplotlib.pyplot as plt

cap = cv.VideoCapture(1)

font = cv.FONT_HERSHEY_SIMPLEX
average_fps = 0
e1 = cv.getTickCount()

#img = cv.imread('car.jpg')
whT = 320
confThreshold = 0.5
nmsThreshold = 0.3

classFile = "coco.names"
classNames = []
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = 'yolov3-320.cfg'
modelWeights = 'C:\models\yolov3.weights'
#modelConfiguration = 'yolov3-tiny.cfg'
#modelWeights = 'C:\models\yolov3-tiny.weights'

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)

net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

def findObjects(outputs, img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    indices = cv.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    for i in indices:
        if isinstance(i, list):
            i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        # have each rectangle be a different color
        cv.rectangle(img, (x, y), (x + w, y + h), (10, 0, 255), 1)
        cv.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%',
                   (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (10, 0, 255), 1)

while True:
    success, img = cap.read()
    
    blob = cv.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    layerNames = net.getLayerNames()
    g = net.getUnconnectedOutLayers()
    outputNames = [layerNames[i - 1] for i in net.getUnconnectedOutLayers()]
    
    outputs = net.forward(outputNames)

    findObjects(outputs, img)
    # putting the FPS count on the frame
    time = (cv.getTickCount() - e1)/ cv.getTickFrequency()
    e1 = cv.getTickCount()
    fps = 1/time
    average_fps = average_fps + (fps - average_fps)/100
    cv.putText(img, str(np.round(fps,1)), (10, 50), font, 1, (255, 255, 0), 2, cv.LINE_AA)
    cv.putText(img, str(np.round(average_fps,1)), (10, 100), font, 1, (125, 0, 255), 2, cv.LINE_AA)


    cv.imshow('Image', img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        # save the last frame
        cv.imwrite('.\images\last_frame.jpg', img)
        break

print(blob.shape)



