import numpy as np
import copy
from deep_translator import (GoogleTranslator,
                            #  ChatGptTranslator,
                            #  MicrosoftTranslator,
                            #  PonsTranslator,
                            #  LingueeTranslator,
                            #  MyMemoryTranslator,
                            #  YandexTranslator,
                            #  PapagoTranslator,
                            #  DeeplTranslator,
                            #  QcriTranslator,
                            #  single_detection, # key: b7033562afd25b4a2865f5d6be90e7ea | pw: language detection
                            #  batch_detection
                             )
import nltk
import re


# ## Too long to run every time
# def translate_news(news_dict):
#     print('Translating news...')
#     trans_dict = {}
#     for site_name in list(news_dict.keys()):
#         trans_item_list = []
#         for item in news_dict[site_name]:
#             trans_item = {}
#             for text_type in list(item.keys()):
#                 translated = GoogleTranslator(source='auto', target='en').translate_batch(item[text_type])
#                 trans_item.update({text_type: translated})
#             trans_item_list.append(trans_item_list)
#         trans_dict.update({site_name: trans_item_list})
#     return trans_dict


def translate_word_list(word_list):
    translated = GoogleTranslator(source='auto', target='en').translate_batch(word_list)   # around 10 words of 1000 chars correspond to ~3.3s and around 3.5s for 4999 (MAX) chars
    return translated


def translate_all_titles(sites_dict):
    concat_titles_dict = {}
    for site_name in list(sites_dict.keys()):
        concat_titles_list = ['']
        for i in range(len(sites_dict[site_name])):
            title_str = sites_dict[site_name][i]['title']
            if len(concat_titles_list[-1]) + len(title_str) >= 5000:
                concat_titles_list.append('')
            concat_titles_list[-1] += '. ' + title_str
        concat_titles_dict.update({site_name: translate_word_list(concat_titles_list)})
    return concat_titles_dict


def translate_all_text(sites_dict):
    concat_titles_dict = {}
    for site_name in list(sites_dict.keys()):
        concat_titles_list = ['']
        for item in sites_dict[site_name]:
            for text_type in list(item.keys()):
                text_str = item[text_type]
                if len(concat_titles_list[-1]) + len(text_str) >= 5000:
                    concat_titles_list.append('')
                concat_titles_list[-1] += '. ' + text_str
        print('Count of characters for ' + site_name + ': ' + str( [len(s) for s in concat_titles_list] ))
        concat_titles_dict.update({site_name: translate_word_list(concat_titles_list)})
    return concat_titles_dict


def filter_keywords_nlp(word_list):
    filtered_list = []
    for word in word_list:
        tokens = nltk.word_tokenize(word)
        tagged = nltk.pos_tag(tokens)
        for tag in tagged:
            if tag[1] in ['NN', 'NNP', 'NNPS', 'NNS'] and len(tag[0])>1:
                filtered_list.append(tag[0])
    return filtered_list


def filter_keywords_all_sites(transl_dict):
    keyword_dict = {}
    for site_name in list(transl_dict.keys()):
        keyword_dict.update({site_name: filter_keywords_nlp(transl_dict[site_name])})
    return keyword_dict


def find_freq_keywords(keyword_dict):
    freq_list, word_vector = [], []
    site_keys = list(keyword_dict.keys())
    for i_site in range(len(site_keys)):
        site_name = site_keys[i_site]
        for w in keyword_dict[site_name]:
            i_vector = -1
            if not w in word_vector:
                word_vector.append(w)
                freq_list.append([0]*len(site_keys))
            else:
                i_vector = word_vector.index(w)
            freq_list[i_vector][i_site] += 1
    return freq_list, word_vector


def find_common_keywords(keyword_dict):
    freq_list, word_vector = find_freq_keywords(keyword_dict)
    common_words = []
    for i in range(len(word_vector)):
        if sum( [val != 0 for val in freq_list[i]] ) >= 3:
            common_words.append(word_vector[i])
    return common_words



