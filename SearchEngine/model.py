import nltk
import cv2
import urllib
import numpy as np
import urllib.parse
import pytesseract

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

# nltk.download("popular")
# nltk.download("stopwords")
# nltk.download("wordnet")


def load_image(image_url):
    urllib.parse.quote(':')

    # Loading the image from external source
    req = urllib.request.urlopen(image_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)  # 'Load it as it is'

    return img


def extract_text(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # use Tesseract to OCR the image
    text = pytesseract.image_to_string(img)

    return text


def preprocess_text(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    new_words = tokenizer.tokenize(text)
    stop_words = set(stopwords.words("english"))

    filtered_words = set()

    for w in new_words:
        if w not in stop_words:
            filtered_words.add(w)

    result = ' '.join([str(word) for word in filtered_words])
    result = result.lower()

    return result


def extract(image_url):
    img = load_image(image_url)

    text = extract_text(img)

    preprocessed_text = preprocess_text(text)

    return preprocessed_text
