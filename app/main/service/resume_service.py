import cv2
from pdf2image import convert_from_path
import pytesseract
import os
import glob
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
import json

stop_words = set(stopwords.words('english'))

cue_words = open("preprocess/cue_word.txt", "r").readlines()
cue_words = [re.sub(r"\n", "", c) for c in cue_words]
cue_words = set(cue_words)

cue_phrases = open("preprocess/cue_phrases.txt", "r").readlines()
cue_phrases = [re.sub(r"\n", "", c) for c in cue_phrases]

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
    remove_words = []
    with open("preprocess/REMOVE_WORD.txt", "r") as rm_file:
        remove_words = rm_file.readlines()
        remove_words = [ re.sub(r"\n", "", remove_word) for remove_word in remove_words ]

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

    sentences = [re.sub(r"(protected data)|(protected@topcv.vn)", "", sen) for sen in sentences]
    sentences = [sen for sen in sentences if len(sen) > 0]

    for w in remove_words:
        sentences = [sentence for sentence in sentences if w not in sentence]

    rm_file.close()

    return sentences

def process_raw_text(sentences):
    sentences = [ (sen.lower(), i) for (sen, i) in sentences ]
    sentences = [ (re.sub(r"[^a-zA-Z\s]+", "", sen), i) for (sen, i) in sentences ]

    sentences = [ (word_tokenize(sen), i) for (sen, i) in sentences ]
    sentences = [ ([word for word in sen if word not in stop_words and len(word) > 1], i) for (sen, i) in sentences ]

    sentences = [ (' '.join(sen), i) for (sen, i) in sentences if len(sen) > 0 ]

    return sentences

def get_topic(educations, experiences, skills, awards, cue_word):
    if cue_word in educations:
        return "EDUCATION"
    elif cue_word in experiences:
        return "EXPERIENCE"
    elif cue_word in skills:
        return "SKILL"
    elif cue_word in awards:
        return "AWARD"
    # elif cue_word in certifications:
    #     return "CERTIFICATION"
    else:
        return ""

def cv_segmentation():
    sentences = parse_pdf()
    educations_cue = experiences_cue = skills_cue = awards_cue = certifications_cue = []

    with open('preprocess/topic.json') as json_file:
        data = json.load(json_file)
        educations_cue = data["Education"]
        experiences_cue = data["Experience"]
        skills_cue = data["Skills"]
        awards_cue = data["Awards"]
        # certifications_cue = data["Certification"]

    index_sentences = [(sentences[i], i) for i in range(len(sentences))]
    index_sentences = process_raw_text(index_sentences)

    topics = []
    cur_topic = ""

    for (sen, id) in index_sentences:
        if (len(sen.split()) == 1 and sen in cue_words) or (len(sen.split()) > 1 and sen in cue_phrases):
            cur_topic = get_topic(educations_cue, experiences_cue, skills_cue, awards_cue, sen)
            topics.append((id,cur_topic))
        else:
            topics.append((id, cur_topic))

    educations = [sentences[topic[0]] for topic in topics if topic[1] == 'EDUCATION']
    experiences = [sentences[topic[0]] for topic in topics if topic[1] == 'EXPERIENCE']
    skills = [sentences[topic[0]] for topic in topics if topic[1] == 'SKILL']
    awards = [sentences[topic[0]] for topic in topics if topic[1] == 'AWARD']
    # certifications = [sentences[topic[0]] for topic in topics if topic[1] == 'CERTIFICATION']

    return {
        'education': '\n'.join(educations),
        'experience': '\n'.join(experiences),
        'skill': '\n'.join(skills),
        'award': '\n'.join(awards),
    }, 200

