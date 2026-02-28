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
    filtered_list = list( filter(lambda x: len(x)>0, list_sentences) ) # remove empty lists
    return filtered_list


def tokenize_sentence(sentence):
    word_separators = '‘’\'\s\-–'
    regex_str = '[' + word_separators + ']+'
    list_words = re.split(regex_str, sentence)
    filtered_list = list( filter(lambda x: len(x)>0, list_words) ) # remove empty lists
    return filtered_list


def convert_sentence_to_indices(word_list, vector):
    # Uses vector indices to convert word_list to sequence of numbers
    converted_list = []
    for w in word_list:
        try:
            converted_list.append(vector.index(w))
        except:
            vector.append(w)
            converted_list.append(len(vector)-1)
    return converted_list, vector


def process_raw_string(string, vector):
    normalized = normalize_chars(string)
    sentences = separate_subexpressions(normalized)
    double_list_words = []
    for sub_sentence in sentences:
        tokenized = tokenize_sentence(sub_sentence)
        converted, vector = convert_sentence_to_indices(tokenized, vector)
        double_list_words.append(converted)
    filtered = list( filter(lambda x: len(x)>0, double_list_words) ) # remove empty lists
    return filtered, vector


def process_site_data(site_dict_list, vector):
    processed_list = []
    for item_dict in site_dict_list:
        proc_item_dict = {}
        for key in list(item_dict.keys()):
            proc_string, vector = process_raw_string(item_dict[key], vector)
            proc_item_dict.update({key: proc_string})
        processed_list.append(proc_item_dict)
    return processed_list, vector
            

def process_data_all_sites(sites_dict):
    processed_dict = {}
    vector = []
    for site_name in list(sites_dict.keys()):
        processed_list, vector = process_site_data(sites_dict[site_name], vector)
        processed_dict.update({site_name: processed_list})
    return processed_dict, vector
