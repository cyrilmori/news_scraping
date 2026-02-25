import pandas as pd
import numpy as np
import unicodedata
import regex
import re


def normalize_chars(string):
    processed_string = unicodedata.normalize('NFKD', string)
    processed_string = processed_string.lower()
    return processed_string


def separate_subexpressions(string):
    list_markers = ',\.:;"!\?\\/#。，“”．…、«»¿¡\(\)\[\]\{\}—'   # most common Latin punctuation chars
    regex_str = '['+list_markers+']+'
    list_sentences = re.split(regex_str, string)
    return list_sentences


def tokenize_sentence(sentence):
    word_separators = '‘’\'\s\-–'
    regex_str = '[' + word_separators + ']+'
    list_words = re.split(regex_str, sentence)
    filtered_list = list( filter(lambda x: len(x)>0, list_words) )
    return filtered_list


def convert_sentence_to_indices(vector, word_list):
    # Uses vector indices to convert word_list to sequence of numbers
    converted_list = []
    for w in word_list:
        try:
            converted_list.append(vector.index(w))
        except:
            vector.append(w)
            converted_list.append(len(vector)-1)
    return vector, converted_list




if __name__ == '__main__':
    normalized = normalize_chars("Municipales à Paris : le candidat Horizons [Pierre-Yves} Bournazel affirme qu’il ne rejoindra « ni Grégoire ni Dati » au second tour ")
    sentences = separate_subexpressions(normalized)
    double_list_words = []
    vector = []
    for sub_sentence in sentences:
        tokenized = tokenize_sentence(sub_sentence)
        vector, converted = convert_sentence_to_indices(vector, tokenized)
        double_list_words.append(converted)
    print(vector, '\n', double_list_words)

