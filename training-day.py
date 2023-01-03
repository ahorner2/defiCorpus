import sklearn
import numpy as np
import csv
import unicodedata as unicode
from sklearn.model_selection import train_test_split

class CorpusReader:
    '''Class to read and ignore unicode errors when printing corpus'''
    def __init__(self, file_path):
        self.file_path = file_path

    def __iter__(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    yield line.strip()
                except UnicodeEncodeError:
                    continue
                
def test_train_split():
    '''Parse data collected in build_corpus into test/train splits'''
    
    reader = CorpusReader('defi-corpus.cor')
    corpus_data = list(reader)

    corpus = []
    for line in corpus_data:
        corpus.append(line)

    train_data, test_data = train_test_split(corpus, test_size=0.2)

    # write train/test data to csv   
    with open('test_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for item in test_data:
            writer.writerow([item])

    with open('train_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for item in train_data:
            writer.writerow([item])
            
    return train_data, test_data
