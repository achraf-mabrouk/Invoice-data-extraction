import pytesseract
from pytesseract import Output
from OCR_text_bboxes import getting_bounding_boxes,get_img_path
import cv2
import re
import os
from pathlib import Path

import string_matching_v5 as sm
import value_detection_v2 as vd

pytesseract.pytesseract.tesseract_cmd =  r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def cleaning_raw_data(d):
    new_d={
        'text':[],
        'left':[],
        'top':[],
        'width':[],
        'height':[],
        'conf':[]
        }
    n_boxes = len(d['text'])
    for i in range(n_boxes) :    
        # r'[a-zA-Z]{2,}|\d'
        if re.match(r'[\w]', d['text'][i]):
            new_d['text'].append(d['text'][i])       
            new_d['left'].append(d['left'][i])
            new_d['top'].append(d['top'][i])
            new_d['width'].append(d['width'][i])
            new_d['height'].append(d['height'][i])
            new_d['conf'].append(d['conf'][i])

    return new_d


# p = Path("~/Dropbox/Memoire/py/factures/")
# data_folder = p.expanduser()

# for i in range(len(os.listdir(data_folder.joinpath("tiff/")))):
#input image preparation
# img_name = str(i)+".tiff"
img_name = "40.tiff"
img_path = get_img_path("tiff/"+img_name)
# read input image
img = cv2.imread(img_path)
# execute tesseract on the image
d = pytesseract.image_to_data(img, config='-l fra --oem 1 --psm 3', output_type=Output.DICT)
# print("before cleaning:",len(d["text"]))
d = cleaning_raw_data(d)
# print("after cleaning:",len(d["text"]))
# keywords to be extracted
query_keys = {"invoice_number":'', "date":'', "total_amount":''}

#get bounding boxes of the text
img = getting_bounding_boxes(img, d)


# Execute key detection process and print out the results
for key,value in query_keys.items():
    result = sm.key_detection(d, key)
    # print('**Matched candidates of the key="%s" : \n%s'%(key,str(result)))

    # draw matched keywords on the image
    img, best_candidate = sm.draw_matched_candidates(img, result)
    query_keys[key] = best_candidate


print("Detected keywords:\n",query_keys)

# test if keyword has been detected or not

if query_keys['invoice_number']:
    img = vd.get_value(d, query_keys['invoice_number'][2], 'alphanumeric', img)
else:
    print("**invoice_number not detected!")
if query_keys['date']:    
    img = vd.get_value(d, query_keys["date"][2], "date", img)
else:
    print("**Date not detected!")
if query_keys['total_amount']:    
    img = vd.get_value(d, query_keys['total_amount'][2], "numeric", img)
else: 
    print("**Total amount not detected!")
    
sm.display_img(img, img_name)
# save result
# result_folder = data_folder / "results"
# cv2.imwrite(os.path.join(result_folder , img_name), img)