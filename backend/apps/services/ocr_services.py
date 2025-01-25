import pytesseract
import cv2

class OCRService:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update this path as needed

    def extract_text(self, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text
