# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:20:42 2021

@author: mabro
"""
import pytesseract
from fuzzywuzzy import fuzz
from pytesseract import Output
from OCR_text_bboxes import getting_bounding_boxes, get_img_path
import cv2
from PIL import Image
pytesseract.pytesseract.tesseract_cmd =  r'C:\Program Files\Tesseract-OCR\tesseract.exe'


    
def generate_candidates(d, query_key):
    n_boxes = len(d['text'])
    keyword_len = len(query_key.split())
    list_of_candidates = []
    index = [0,1,-1]
    for x in index:
        l = keyword_len + x
        if l == 0: 
            continue
        else:
            for i in range(n_boxes-l+1):
                ngram=""
                if int(d['conf'][i]) > 60:
                    # get ngram starts from the position i 
                    temp=[d['text'][j].lower() for j in range(i,i+l)]
                    ngram = " ".join(temp)
                    # string distance
                    ratio = fuzz.ratio(query_key, ngram)   
                    # select the best scored ones
                    if ratio >= 75: 
                        # calculate width if the keyword composed by 2 or more words
                        space_width = 13
                        new_width = space_width *(l-1)
                        for j in range(i, i+l):
                            new_width += d['width'][j] 
                        
                        (x, y, w, h) = (d['left'][i] , d['top'][i], new_width, d['height'][i])
                        list_of_candidates.append([ngram, ratio, (x, y, w, h)])
    return list_of_candidates

# keyword dictionary of equivalent keywords
keywords = {
    'invoice_number': ["facture n°", "numero n°", "n° piece", "n° facture", "numero de facture", "bon de livraison"],
    'date': ["date de facturation", "date", "tunis, le"],
    'total_amount': ["total ttc", "net a payer", "total a payer ttc", "montant ttc"]
    
    }

keywords_en = {
    'invoice_number': ["invoice number"],
    'date': ["date of issue", "invoice date", "date"],
    'total_amount': ["amount due", "total amount", "amount paid"]
    
    }

def key_detection(d, key):
    list_of_equiv = keywords[key]
    detected_candidates = []
    for i in range(len(list_of_equiv)):
        matched_candidates = generate_candidates(d, list_of_equiv[i])
        
        if matched_candidates :
            detected_candidates.extend(matched_candidates)   
    
    return detected_candidates


def get_highest_scored_candidate(list_candidates):
    best_score_index = 0
    for i in range(1, len(list_candidates)):
        if list_candidates[best_score_index][1] < list_candidates[i][1]:
            best_score_index = i

    return list_candidates[best_score_index]
        

def draw_matched_candidates(img, detected_candidates):
    best_candidate = []
    if detected_candidates:
        best_candidate = get_highest_scored_candidate(detected_candidates)
        # draw best candidate
        (x, y, w, h) = best_candidate[2]
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
                            
    return img,best_candidate


def display_img(img, img_name):
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img2)
    im_pil.show()

    
def main():
    # input image
    img_name = "tiff/53.tiff"
    img_path = get_img_path(img_name)
    # read input image
    img = cv2.imread(img_path)
    # keywords to be extracted
    query_keys = ["invoice_number", "date", "total_amount"]
    
    # execute tesseract
    d = pytesseract.image_to_data(img, config='-l fra --oem 1 --psm 3', output_type=Output.DICT)

    #get bounding boxes of the text
    img = getting_bounding_boxes(img, d)
    
    # Execute key detection process and print out the results
    for key in query_keys:
        result = key_detection(d, key)
        print('**Matched candidates of the key="%s" : \n%s'%(key,str(result)))

        # draw matched keywords on the image
        img,best_candidate = draw_matched_candidates(img, result)
        
    display_img(img, img_name)
    
  
# main()

