import pytesseract
from pytesseract import Output
from OCR_text_bboxes import get_img_path
import cv2
import re

pytesseract.pytesseract.tesseract_cmd =  r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_value(d, key_coord, nature, img):
    (x, y , w, h) = key_coord
    key_centroid = (x+(w/2), y+(h/2)) 
    
    for i in range(len(d["text"])):    
        (x1, y1, w1, h1) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
        bb_centroid = (x1+(w1/2), y1+(h1/2)) 
        
        # horizontal search
        if(bb_centroid[0] > key_centroid[0] and abs(key_centroid[1] - bb_centroid[1])<50):
            
            if nature == "date":                     
                if re.match(r'\d{2,4}[-/]\d{1,2}[-/]\d{1,4}', d["text"][i]):                         
                    img = draw_bb_value(img, (x1, y1, w1, h1))
                    # print(d["text"][i])
                    
            elif nature == "numeric":
                    # match currency 
                    if re.match(r'^\$?\d+([.,]?\d*)*', d["text"][i]):
                        img = draw_bb_value(img, (x1, y1, w1, h1))
                        # print(d["text"][i])
                        
            elif nature == "alphanumeric" and abs(key_centroid[0] - bb_centroid[0])<520 :
                if re.match(r'^#?([a-zA-Z])*[/-]?\d+', d["text"][i]):
                    img = draw_bb_value(img, (x1, y1, w1, h1))
                    # print(d["text"][i])


        # vertical search
        if(abs(key_centroid[0] - bb_centroid[0])<40 and (bb_centroid[1] > key_centroid[1]) 
           and abs(key_centroid[1] - bb_centroid[1])<200):
            
            if nature == "date":
                if re.match(r'\d{2,4}[-/]\d{1,2}[-/]\d{1,4}', d["text"][i]):                        
                    img = draw_bb_value(img, (x1, y1, w1, h1))
                    # print(d["text"][i])
                    
            elif nature == "numeric":
                    # match currency 
                    if re.match(r'^\$?\d+([.,]?\d*)*', d["text"][i]):
                        img = draw_bb_value(img, (x1, y1, w1, h1))
                        # print(d["text"][i])
                        
            elif nature == "alphanumeric":
                if re.match(r'^#?([a-zA-Z])*[/-]?\d+', d["text"][i]):                        
                    img = draw_bb_value(img, (x1, y1, w1, h1))
                    # print(d["text"][i])

    return img 

def draw_bb_value(img, val_coord):
    
    (x, y, w, h) = val_coord
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
    return img



def main():
    # input image preparation
    img_name = "tiff/img15.tiff"
    img_path = get_img_path(img_name)
    # read input image
    img = cv2.imread(img_path)
    # execute tesseract on the image
    d = pytesseract.image_to_data(img, config='-l fra --oem 1 --psm 3', output_type=Output.DICT)


    # total_tva_img0 = (1759, 2423, 213, 31)
    # key_alphanumeric_img0 = (174, 1105, 245, 37)
    # total_tva_img4 = (1477, 2845, 209, 29)
    # total_ttc_img4 = (1759, 2543, 207, 31)
    # total_tva_img11 = (1866, 2046, 171, 28)
    # total_ttc_img11 = (1868, 2196, 169, 30)
    # numero_img7 = (156, 588, 187, 31)
    # total_ttc_img7 =(1654, 3023, 238, 29)
    date_img15 = (318, 708, 81, 30)
    total_ttc_img15 = (1758, 2906, 182, 45)
    # net_apayer_coord_img16 = (1915, 2560, 207, 28)


    
    print("Date :")
    get_value(d, date_img15, "date", img)
    # # print("**Invoice number :")
    # get_value(d, numero_img7, 'alphanumeric')
    
    print("**Total :")
    img = get_value(d, total_ttc_img15, "numeric", img)
    print("\n")
    
    
# main()    