import cv2
import pytesseract
from pytesseract import Output
from pathlib import Path
pytesseract.pytesseract.tesseract_cmd =  r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_img_path(img_name):
    p = Path("~/Dropbox/Memoire/py/factures")
    data_folder = p.expanduser()
    img_path = data_folder / img_name
    img_path = str(img_path)
    
    return img_path

def getting_bounding_boxes(input_img, d):
    
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            output_img = cv2.rectangle(input_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return output_img

def main():
    # input image preparation
    img_name = "tiff/info3000.bmp"
    img_path = get_img_path(img_name)
    # read input image
    img = cv2.imread(img_path)
    
    d = pytesseract.image_to_data(img, lang="fra", config='--oem 1 --psm 3', output_type=Output.DICT)
    
    output_img = getting_bounding_boxes(img, d)
    
    
    cv2.namedWindow(img_name,cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(img_name, 800,800)
    cv2.imshow(img_name, output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
# main()      