import json
import os
import re
import sys

class Document:
    def __init__(self, term_counts):
        self.term_counts = term_counts

    def __str__(self):
        terms = sorted(self.term_counts.items())
        return f"{len(terms)} " + " ".join(f"{term}:{count}" for term, count in terms)

class Corpus:
    def __init__(self):
        self.documents = []
        self.labels = []

    def add_document(self, doc, label):
        self.documents.append(doc)
        self.labels.append(label)

    def save_data(self, data_path, label_path):
        with open(data_path, 'w') as data_file:
            for doc in self.documents:
                data_file.write(str(doc) + '\n')

        with open(label_path, 'w') as label_file:
            for label in self.labels:
                label_file.write(f"{label}\n")

def read_non_stop_words(filepath):
    with open(filepath, 'r') as file:
        return {word.strip(): idx for idx, word in enumerate(file)}

def normalize_text(text):
    # Convert to lowercase
    text = text.lower()
    # Replace hyphens with spaces to separate joined words
    text = re.sub(r'-', ' ', text)
    # Remove all non-alphabetic characters except single quotes for contractions
    text = re.sub(r"[^a-z\s']", '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_json_data(json_path, non_stop_words):
    with open(json_path, 'r') as file:
        data = json.load(file)
    corpus = Corpus()
    for article in data:
        # Normalize the article body text
        normalized_text = normalize_text(article['body'])
        words = normalized_text.split()
        word_counts = {}
        for word in words:
            # Handle possessive cases and other contractions
            word = word.rstrip("'s")  # stripping possessive 's
            if word in non_stop_words:
                word_index = non_stop_words[word]
                if word_index not in word_counts:
                    word_counts[word_index] = 0
                word_counts[word_index] += 1
        doc = Document(word_counts)
        corpus.add_document(doc, article['true_narrative'])
    return corpus

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 process.py [json file path] [non-stop words path] [output directory]")
        sys.exit(1)

    json_file_path = sys.argv[1]
    non_stop_words_path = sys.argv[2]
    output_dir = sys.argv[3]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    non_stop_words = read_non_stop_words(non_stop_words_path)
    corpus = process_json_data(json_file_path, non_stop_words)
    data_file_path = os.path.join(output_dir, 'data.dat')
    label_file_path = os.path.join(output_dir, 'label.dat')
    corpus.save_data(data_file_path, label_file_path)
