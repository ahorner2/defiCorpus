import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.cluster.util import cosine_distance
import gensim
from gensim import utils
from gensim.test.utils import datapath

class CorpusReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_corpus(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()

def corpus_word_freq():
    corpus_reader = CorpusReader('defi-corpus.cor')
    
    corpus = []
    for line in corpus_reader.read_corpus():
        corpus.extend(line)
        
    # weighted frequency
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for sentence in corpus:
        for word in nltk.word_tokenize(sentence):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

    for word in word_frequencies.keys():
        maximum_frequncy = max(word_frequencies.values())
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        
    return word_frequencies

def main():
    
    reader = corpus_word_freq()
    corp_data = list(reader)
    for line in corp_data:
        print(line)

if __name__ == '__main__':
    main()

