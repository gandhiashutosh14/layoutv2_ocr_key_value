from layout_lm_sub_file.index_reset import *
from layout_lm_sub_file.generate_mapping_and_training_dict import *
from google.cloud import vision
from layout_lm_sub_file.combine_words import *
from google.cloud.vision_v1 import types
import io
from PIL import Image, ImageDraw, ImageOps
from for_linking import *
from enum import Enum
import shutil




from google.oauth2 import service_account
import json
service_account_info_string = R"""{
  "type": "service_account",
  "project_id": "vision-testing-362404",
  "private_key_id": "a111789c76d0b74397a9988adf60c7494a0d7241",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQC+9rpTJ0xtAegf\nLI5BzMbr6Du3ES/zyarwBNwV56QFo4KwMFeT/idd534lQH0orJGn0hbRKes9yAHK\n0olO0fm6eRMRp+MQbJH+sfHgmytf7nACH6K7BgKub5g4z/IbNIqr+k3dDUox6y+X\ngKIuTjisnydy4OPiC5oIfrP4dG4h4Zyzlf2yM+NBtg9lWVoP46/dk7/WqSKS+rip\nJwO4DyU3vFiA2DHPEa67IdblSRrMJoALa9sdvWbQTKbzhQosAeLQgDQO883Wl1GP\novUc33X6PljA8sWKUmHku0i/ZuvnG7Vu5L/5jI1sUz2rVbBUtMlMNehPoNwR5JDh\nR+UdsmJlAgMBAAECggEAD3HcEwKgK0bWs8LCRK8fvY+8WKuSschzQ1NZS4o/GVem\np8JZKvaIz478BF5JYSNH6odS4hreVFJbVsCda1sPNBY7xRdLhZYKXsuckPpr0Sfz\nNjDB1BeB2wLakGm9HpcqygsGBiVfhVcMs9erBky8R7Xdlmx68drXW+2Hd8ZO6/1z\n0o4bACKRgazN65I3NVPy5k8lZWcXkNwhX6f3/OfFP6WkeC0wl4E7zKYikBzfqVJh\n/Us+uXjUB/w1CZDbbbajAj4PLjznHJxgal0/Mp1YnGVLI+tMvvTB35iFwSzdyDvG\nbmdkI3jKEG+vhVUS76vSk6OtwiJkV6JZQMNVmvs0UQKBgQD4KSLfvs335nkKzFdX\n3V5kiioMarxNHIQrzm/+dztfU02TNsaJZPa4hSrOmWQS10O850Z+/pBFEuZLLPkg\nL421Pqz8UuvQ3IpzdbIDn1Tkd/3Lf6EymV9cadV6AJMI9glx1wyTYVtPUQjBKXFi\nfZ1ErQgzosqA8bWOzDSxzB43TQKBgQDE/wr8OkVojjN/sH94t4Yg4li9FCUyxofU\nUhCzowcCUPZJj3C+CtK36bTnM2k1J0gr8BggIEKsGLf0q/bFqcQAtQ3/0ORBY6cm\n8juh1KS145/K2R67qusDJQ3goUm76aF7WAEB7jBxpzI+QFLX+53FzQZGo4I5H4W7\nP7eilJm7eQKBgAaoI9VYqvHBbvHJNXaX65ZK1oHqww5We30pVnu++wq9k1EloQHC\ngZPFjrZoCvUubRS+J3f0oC4aKa9Oj4g7flOkUMOb/dNmdxhNye6q8X4HcflpfQt8\nbcBu3lkddtRAtVQmbqHtdKOWCuQTloUL1ZIoChZIgaIf2bzw4WD7lrvpAoGBAK+H\nPSePWGcYRcTh5EMQ67+DT2Ryfc6nXUIPOXiGq+khcMIMwH1lMWrUH+/ePEEzVjho\nP2bot9+WStsFGuX3JYEn0mh9ndSx0a9/KSlCSt0TDD93hM3dNnhf3OSpcgSw4MUB\nniw1Kw8p1jfnoql2NpeX3p60dIUnlEZLOPnxhKWpAn8ZrZhBuVEX8XDsyleONbSB\nLcqCaA0U9IIn1DH2BWWzu7O7lS7s2Gu9T7g8wbmhkCEZEAXqOKg8iYmy7r3fO3qc\nm0kq1cL2kOjrbjWNxZBX+rWxyzNH6s+TD3yxlmx/wneXgnGhx6nIgIJ3UiiYCBc4\nCAOOVfiQUuPDDFNubzzd\n-----END PRIVATE KEY-----\n",
  "client_email": "vision-testing-362404@appspot.gserviceaccount.com",
  "client_id": "106824030292938353307",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vision-testing-362404%40appspot.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""
service_account_info_json = json.loads(service_account_info_string)
service_account_creds = service_account.Credentials.from_service_account_info(service_account_info_json)
def image_ocr(image_path,training_image_folder):
    image  = Image.open(image_path)
    if "/" in image_path:
        image_path2 = image_path.split("/")
        image_path2 = image_path2[-1] 
    else:
        image_path2 = image_path
    image.save(training_image_folder+"/"+image_path2)


    document,response = generate_ocr(image_path)

    bounds,list_of_word,list_of_word_bounding_box = get_document_bounds(document, FeatureType.WORD)
    draw_boxes(image_path,training_image_folder,bounds, 'yellow')
    generate_main_list = generate_main_dict(list_of_word,list_of_word_bounding_box)
    return generate_main_list

def generate_ocr(image_file):
    client = vision.ImageAnnotatorClient(credentials=service_account_creds)
    with io.open(image_file, 'rb') as image_file1:
            content = image_file1.read()
    content_image = types.Image(content=content)
    response = client.document_text_detection(image=content_image)
    document = response.full_text_annotation

    return document,response



class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5
    
def draw_boxes(image_path,training_image_folder,bounds, color,width=5):
    image  = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y],fill=color, width=width)
    
    # image  = Image.open(image_path)
    if "/" in image_path:
        image_path2 = image_path.split("/")
        image_path2 = image_path2[-1] 
    else:
        image_path2 = image_path
    image.save(training_image_folder+"annotated_images/"+image_path2)
    return image

def get_document_bounds(document, feature):
    bounds=[]
    list_of_word=[]
    list_of_word_bounding_box=[]
    for i,page in enumerate(document.pages):
        for block in page.blocks:
            if feature==FeatureType.BLOCK:
                bounds.append(block.bounding_box)
            for paragraph in block.paragraphs:
                if feature==FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)
                for word in paragraph.words:
                    present_word = "" # empty string
                    for symbol in word.symbols:
                        present_word += symbol.text
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)
                    list_of_word.append(present_word)
                    
                    # print((present_word, str(word.bounding_box.vertices)))
                    sub_box=[]
                    for i in word.bounding_box.vertices:                
                        sub_box.append([i.x,i.y])
                    list_of_word_bounding_box.append(sub_box)
                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)
    return bounds,list_of_word,list_of_word_bounding_box


def generate_main_dict(list_of_word,list_of_word_bounding_box):
    main_list = []
    for i in range (0,len(list_of_word)):
        dict_00 = {}
        dict_00["word"] = list_of_word[i]
        dict_00['Coordinate']= list_of_word_bounding_box[i]
        main_list.append(dict_00)
    return main_list
        





main_listing = image_ocr("IMG_5889.jpg","D:/Python_scripts/OCR/final_testing/")
map_123 , training  = generate_dict_and_mapping_dict_from_main_list(main_listing)
# print("for selection of the words:",training)
# print("====="*80)
# print(map_123)


training = combine_words(["Batch","No."],map_123,training)
training = index_reset(training)

print(training)