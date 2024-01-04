import gradio as gr
from PIL import Image, ImageDraw, ImageFont
from layout_lm_tutorial.layoutlm_preprocess import *


logo_image_path = "D:/Python_scripts/OCR/docquery/LOGO.png"
logo_image = Image.open(logo_image_path)
def transform_elements(list_of_lists):
    transformed_list_of_lists = [
        [abs(element) if element < 0 else min(element, 998) for element in sub_list]
        for sub_list in list_of_lists
    ]
    return transformed_list_of_lists

def find_sublist_index(main_list, sublist):
    try:
        index = main_list.index(sublist)
        return index
    except ValueError:
        return -1 

def remove_duplicate_sublists(list_of_sublists):
    unique_sublists = []
    seen_sublists = set()

    for sublist in list_of_sublists:
        tuple_sublist = tuple(sublist)

        if tuple_sublist not in seen_sublists:
            unique_sublists.append(sublist)
            seen_sublists.add(tuple_sublist)

    return unique_sublists

def iob_to_label(label):
    if label != 'O':
        return label[2:]
    else:
        return ""

def detect_labels(file):
    num_labels = 7  # number of labels

    model_path = 'D:/Python_scripts/OCR/layout_training_on_local/layoutlm_40.pt'
    model = model_load(model_path, num_labels)
    
    # Load the image from the uploaded file
    image = Image.open(file.name)
    
    image,words, boxes, actual_boxes = preprocess(file.name)
    boxes = transform_elements(boxes)
    word_level_predictions, final_boxes, confidence_list = convert_to_features_2(image, words, boxes, actual_boxes, model)
    final_boxes = list(map(lambda lst: eval(f"[{lst[3][0]},{lst[3][1]},{lst[1][0]},{lst[1][1]}]"), final_boxes))

    final_boxes = [[min(box[0], box[2]), min(box[1], box[3]), max(box[0], box[2]), max(box[1], box[3])] for box in
                   final_boxes]
    labels = ['B-BATCH', 'E-BATCH', 'I-BATCH', 'O', 'S-BATCH', 'S-EXPIRY_DATE', 'S-MFG_DATE']

    label_map = {i: label for i, label in enumerate(labels)}

    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    label_detection_box = []

    label2color = {'mfg_date': 'blue', 'batch': 'yellow', 'expiry_date': 'black', '': 'purple'}
    unique_list_of_sublists = remove_duplicate_sublists(final_boxes)
    output_text = ""
    
    for prediction, box, confidence in zip(word_level_predictions, final_boxes, confidence_list):
        predicted_label = iob_to_label(label_map[prediction]).lower()
        if predicted_label != "":
            index_on_words = find_sublist_index(unique_list_of_sublists, box)
            output_text += f"words: {words[index_on_words]}, predicted_label: {predicted_label}, predicted_confidence: {confidence}, box_coordinates: {box}\n"
            label_detection_box.append(box)
            draw.rectangle(box, outline=label2color[predicted_label])
            draw.text((box[0] + 10, box[1] - 10), text=predicted_label, fill=label2color[predicted_label], font=font)

    return image, output_text
# with gr.Blocks(title="Gradio") as demo:    

#     iface = gr.Interface(fn=detect_labels, inputs="file", outputs=["image", "text"])
# demo.launch()

# with gr.Blocks(title="Gradio") as demo:
#     iface = gr.Interface(fn=detect_labels, inputs="file", outputs=["image", "text"])
# demo.launch(favicon_path  = "D:/Python_scripts/OCR/docquery/LOGO.png",share_server_protocol = 'https')

# with gr.Blocks(title=title) as demo:
#    gr.Interface(....)
# demo.launch()

# import gradio as gr
# from PIL import Image, ImageDraw

# Your custom CSS
CSS = """
#question input {
    font-size: 16px;
}
#url-textbox {
    padding: 0 !important;
}
#short-upload-box .w-full {
    min-height: 10rem !important;
}
/* I think something like this can be used to re-shape
 * the table
 */
/*
.gr-samples-table tr {
    display: inline;
}
.gr-samples-table .p-2 {
    width: 100px;
}
*/
#select-a-file {
    width: 100%;
}
#file-clear {
    padding-top: 2px !important;
    padding-bottom: 2px !important;
    padding-left: 8px !important;
    padding-right: 8px !important;
	margin-top: 10px;
}
.gradio-container .gr-button-primary {
    background: linear-gradient(180deg, #CDF9BE 0%, #AFF497 100%);
    border: 1px solid #B0DCCC;
    border-radius: 8px;
    color: #1B8700;
}
.gradio-container.dark button#submit-button {
    background: linear-gradient(180deg, #CDF9BE 0%, #AFF497 100%);
    border: 1px solid #B0DCCC;
    border-radius: 8px;
    color: #1B8700
}

table.gr-samples-table tr td {
    border: none;
    outline: none;
}

table.gr-samples-table tr td:first-of-type {
    width: 0%;
}

div#short-upload-box div.absolute {
    display: none !important;
}

gradio-app > div > div > div > div.w-full > div, .gradio-app > div > div > div > div.w-full > div {
    gap: 0px 2%;
}

gradio-app div div div div.w-full, .gradio-app div div div div.w-full {
    gap: 0px;
}

gradio-app h2, .gradio-app h2 {
    padding-top: 10px;
}

#answer {
    overflow-y: scroll;
    color: white;
    background: #666;
    border-color: #666;
    font-size: 20px;
    font-weight: bold;
}

#answer span {
    color: white;
}

#answer textarea {
    color:white;
    background: #777;
    border-color: #777;
    font-size: 18px;
}

#url-error input {
    color: red;
}
footer {visibility: hidden}

#logo-image {
    max-width: 10%;
    max-height: 100px;  # Adjust the height as needed
    margin-top: 20px;
    margin-left: ; 
}
"""

# Your Gradio UI components
with gr.Blocks(title="Unicloud pvt ltd",css=CSS) as demo:
    gr.Image(logo_image, elem_id="logo-image",show_label=False, show_download_button= False  ) ,gr.Markdown("# Unicloud :OCR key value pair Engine")
    
    gr.Interface(
        fn=detect_labels,  # Replace with your detect_labels function
        inputs="file",
        outputs=["image", "text"],
        elem_id="gr-interface",     
    )
demo.launch(favicon_path="D:/Python_scripts/OCR/docquery/favlogo.png", share_server_protocol=['https'])
