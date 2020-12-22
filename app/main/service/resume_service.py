import cv2
from pdf2image import convert_from_path
import pytesseract
import os
import glob

def pre_processing(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return threshold_img

def parse_text(threshold_img):
    tesseract_config = r'--oem 3 --psm 1'
    details = pytesseract.image_to_data(threshold_img, output_type=pytesseract.Output.DICT, config=tesseract_config, lang="eng")

    return details

def remove_temp_files(directory):
    files = glob.glob(directory)
    for f in files:
        os.remove(f)

def format_text(details):
    parse_text = []
    word_list = []
    last_word = ''
    for word in details['text']:
        if word != '':
            word_list.append(word)
            last_word = word
        if (last_word != '' and word == '') or (word == details['text'][-1]):
            parse_text.append(word_list)
            word_list = []

    return parse_text

def convert_pdf_to_jpg(filename):
    remove_temp_files('temp/*')

    images = convert_from_path(filename, poppler_path="library/poppler-20.12.1/bin")

    for img in images:
        index = images.index(img)

        img.save('temp/CV_{}.jpg'.format(index), 'JPEG')


def parse_pdf():
    convert_pdf_to_jpg("temp_pdf/CV.pdf")

    img_directory = "temp"
    sentences = []

    for img in os.listdir(img_directory):
        img_name = os.fsdecode(img)
        img_fname = os.path.join(img_directory, img_name)

        image = cv2.imread(img_fname)

        thresholds_image = pre_processing(image)

        parsed_data = parse_text(thresholds_image)

        arranged_text = format_text(parsed_data)
        arranged_text = [ sen for sen in arranged_text if len(sen) > 0 ]

        for sen in arranged_text:
            sentences.append(' '.join(sen).strip())

    sentences = [sen for sen in sentences if len(sen) > 0]
    return sentences

