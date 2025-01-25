import cv2
import pytesseract
import numpy as np
import os

class ImageProcessingService:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update this path as needed
        model_path = os.path.join(os.path.dirname(__file__), '..', 'model')
        cfg_path = os.path.join(model_path, 'yolov3.cfg')
        weights_path = os.path.join(model_path, 'yolov3.weights')
        names_path = os.path.join(model_path, 'coco.names')

        print(f"Loading YOLO config from: {cfg_path}")
        print(f"Loading YOLO weights from: {weights_path}")
        self.net = cv2.dnn.readNet(weights_path, cfg_path)

        self.classes = []
        with open(names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.layer_names = self.net.getLayerNames()
        self.output_layers = self.net.getUnconnectedOutLayers()

        if isinstance(self.output_layers, np.ndarray):
            self.output_layers = [self.layer_names[i - 1] for i in self.output_layers.flatten()]
        else:
            self.output_layers = [self.layer_names[i[0] - 1] for i in self.output_layers]

        print(f"Output layers: {self.output_layers}")

    def process_image(self, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text

    def describe_image(self, image_path):
        image = cv2.imread(image_path)
        height, width, channels = image.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        # Showing information on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        descriptions = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                descriptions.append(f"Detected {label} at location ({x}, {y})")

        if descriptions:
            return " and ".join(descriptions)
        else:
            return "No significant issues detected in the image."

# Example usage
# image_service = ImageProcessingService()
# description = image_service.describe_image("example.jpg")
# print(description)
