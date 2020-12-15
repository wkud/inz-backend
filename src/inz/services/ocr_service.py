import pytesseract
import cv2
from inz.utility.image_utility import ImageUtility
from inz import app

pytesseract.pytesseract.tesseract_cmd = \
    app.config['ABSOLUTE_PATH_TO_TESSERACT_EXECUTABLE']


class OcrUtility:
    @staticmethod
    def recognize(filename, show_image=False):
        path = r'static/receipts/' + filename

        img = ImageUtility.load_image(path, filename, show=show_image)

        recognized_text = pytesseract.image_to_string(img)
        recognized_text = recognized_text.strip()
        print('ocr done')
        return recognized_text


def run_as_main():
    filename = 'thre2.png'

    text = OcrUtility.recognize(filename, True)
    print(text)

    key = cv2.waitKey(1) & 0xFF
    while key != ord('q'):
        key = cv2.waitKey(1) & 0xFF


if __name__ == '__main__':
    run_as_main()
