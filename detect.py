
import cv2
import numpy as np
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
pic_path = os.path.join(dir_path, "pics")
img_path = os.path.join(dir_path, "detect_cfg")

def detect():
    def get_output_layers(net):
        
        layer_names = net.getLayerNames()
        
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers




        
    image = cv2.imread(os.path.join(pic_path, "img.jpg"))

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None

    with open(os.path.join(img_path, "yolov3.txt"), 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    net = cv2.dnn.readNet(os.path.join(img_path, "yolov3.weights"), os.path.join(img_path, "yolov3.cfg"))

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []


    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                class_ids.append(class_id)
                confidences.append(float(confidence))
    last = -1
    name = None
    for i in range(len(class_ids)):
        if confidences[i] > last:
            last = confidences[i]
            name = i

    if name != None:
        return [classes[class_ids[name]], classes[class_ids[name]]]
    else:
        return ["test", "test"]
