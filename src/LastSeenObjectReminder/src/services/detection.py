# src/images/12.jpg
from math import log
import time
import os
import cv2
import numpy as np
from PIL import Image


LSOR = os.path.abspath('./src/LastSeenObjectReminder/src/model-data/model-cfg/LSOR-obj.cfg')
weights = os.path.abspath('./src/LastSeenObjectReminder/src/model-data/weights/yolov4-obj_best.weights')
classNames = os.path.abspath('./src/LastSeenObjectReminder/src/model-data/classes/classes.names')



def saveLog(name,log):
    with open(r"C:\Users\Yoel\Desktop\DL-FinalProject\DL-FinalProject\dl-backend\{0}.txt".format(name), "w") as f:
        f.write(log)
    
def moshe():
    return "Done"


def detectByImage(image_BGR):
    try:
        h, w  = image_BGR.shape[:2]
        blob = cv2.dnn.blobFromImage(image_BGR, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)                             
        with open(classNames) as f:
            labels = [line.strip() for line in f]
        network = cv2.dnn.readNetFromDarknet(LSOR,weights)
        layers_names_all = network.getLayerNames()
        layers_names_output = \
            [layers_names_all[i[0] - 1] for i in network.getUnconnectedOutLayers()]

        probability_minimum = 0.5
        threshold = 0.3
        colours = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')
        network.setInput(blob)  # setting blob as input to the network
        start = time.time()
        output_from_network = network.forward(layers_names_output)
        end = time.time()
        # print('Objects Detection took {:.5f} seconds'.format(end - start))

        bounding_boxes = []
        confidences = []
        class_numbers = []
        
        for result in output_from_network:
            for detected_objects in result:
                scores = detected_objects[5:]
                class_current = np.argmax(scores)
                confidence_current = scores[class_current]

                if confidence_current > probability_minimum:
                    box_current = detected_objects[0:4] * np.array([w, h, w, h])
                    x_center, y_center, box_width, box_height = box_current
                    x_min = int(x_center - (box_width / 2))
                    y_min = int(y_center - (box_height / 2))

                    # Adding results into prepared lists
                    bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
                    confidences.append(float(confidence_current))
                    class_numbers.append(class_current)

        results = cv2.dnn.NMSBoxes(bounding_boxes, confidences,
                                   probability_minimum, threshold)
        
        counter = 1
        if len(results) > 0:
            for i in results.flatten():
                counter += 1

                x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
                box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]

                colour_box_current = colours[class_numbers[i]].tolist()

                cv2.rectangle(image_BGR, (x_min, y_min),
                              (x_min + box_width, y_min + box_height),
                              colour_box_current, 2)

                text_box_current = '{}: {:.4f}'.format(labels[int(class_numbers[i])],
                                                       confidences[i])

                cv2.putText(image_BGR, text_box_current, (x_min, y_min - 5),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, colour_box_current, 2)

                lable = labels[int(class_numbers[i])]
        saveLog('image_BGR',str(type(image_BGR)))
        image = Image.fromarray(image_BGR)
        return (image,lable)
    except Exception as error:
        
        return str(error)