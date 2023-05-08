import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import re
import string
from flask import Flask, request

app = Flask(__name__)

def split_words(text):

    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    text = re.sub(r'\.', ' ', text)

    return text.split()

def get_word_frequencies(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    words = split_words(soup.get_text())

    word_counts = defaultdict(int)
    for word in words:
        if len(word) < 45 and word.isalnum:
            word = re.sub(f'[{re.escape(string.punctuation)}]', '', word)
            word_counts[word] += 1

    return word_counts

@app.route('/analyze', methods=['POST'])
def analyze_webpage():
    url = request.json['url']
    word_frequencies = get_word_frequencies(url)
    word_frequencies_json = json.dumps(word_frequencies, indent=4)

    return word_frequencies_json

if __name__ == '__main__':
    app.run()
