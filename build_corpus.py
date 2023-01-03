import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
import heapq
import csv
import datetime
# ntlk type beats
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

'''Scrapes DeFi Governance forums to build a DeFi native corpus for use in Web3 governance.

Protocols scraped on first pass: Maker, Aave, Comp, Uni, Yearn, and Frax.'''

MAP = {
    
    'MakerDAO': 'https://forum.makerdao.com/top?period=yearly',
    'Aave': 'https://governance.aave.com/top?period=yearly',
    'Compound': 'https://www.comp.xyz/top?period=yearly',
    'Uniswap': 'https://gov.uniswap.org/top?period=yearly',
    'Yearn': 'https://gov.yearn.finance/top?period=yearly',
    'Frax': 'https://gov.frax.finance/top?period=yearly',

}

def build_corpus(MAP):
    for doc in MAP.keys():
        url = MAP[doc]
        protocol = url.split('.')[1]

        print(f'Scraping {url} from {protocol}'.format(url, protocol))

        page = requests.get(url).text  # driver used instead
        soup = BeautifulSoup(page, 'html.parser')

        # page = requests.get(url).text # driver used instead
        soup = BeautifulSoup(page, 'html.parser')

        links = []
        sents = []
        # first page post links
        top_line = [a['href'] for a in soup.findAll('a', class_='title') if a.stripped_strings]  

        for line in top_line:
            links.append(line)

        for link in links:
            res = requests.get(link).text
            souped = BeautifulSoup(res, 'html.parser')

            for content in souped.findAll('div', itemprop='articleBody'):
                article = content.text
                # strip brackets and extra space
                article_text = re.sub(r'\[[0-9]*\]', ' ', article)
                article_text = re.sub(r'\s+', ' ', article_text)
                # strip special chars and digits
                formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
                # split the text into sentences
                sentence_list = nltk.sent_tokenize(article_text)

                for sentence in sentence_list:
                    sents.append(sentence)
                    
                    # tokenize the sentence
                    tokens = nltk.word_tokenize(sentence)
                    # append tokens to corpus with each sent on a new line
                    with open('defi-corpus.cor', 'a', encoding='utf-8') as f:
                        for token in tokens:
                            try:
                                # replace unsupported unicode with ?
                                filtered_token = token.encode('utf-8', errors='replace')
                                # decode back to str format
                                filtered_token = filtered_token.decode('utf-8')
                            except UnicodeError:
                                continue
                            
                            f.write(filtered_token)
                            f.write(' ')
                        f.write('\n')

                # yield sents
            


def main():
   build_corpus(MAP)

if __name__ == '__main__':
    main()
