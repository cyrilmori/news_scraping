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


def concat_all_text(sites_dict):
    concat_titles_dict = {}
    for site_name in list(sites_dict.keys()):
        concat_titles_list = ['']
        for i_art in range(len(sites_dict[site_name])):
            item = sites_dict[site_name][i_art]
            all_text = '$'.join(list(item.values()))
            all_text = re.sub('\n', ' ', all_text)
            all_text = re.sub('\$', '. \n', all_text)
            if len(concat_titles_list[-1]) + len(all_text) >= 5000:
                concat_titles_list.append('')
            block_pointer, text_pointer = len(concat_titles_list)-1, len(concat_titles_list[-1])
            concat_titles_list[-1] += '\n\n' + all_text
        concat_titles_dict.update({site_name: concat_titles_list})
    return concat_titles_dict


def deconcat_all_text(concat_dict):
    deconcat_dict = {}
    for site_name in list(concat_dict.keys()):
        text_list = []
        for block in concat_dict[site_name]:
            article_list = block.split('\n\n')
            for i in range(len(article_list)):
                split_article = article_list[i].split('\n')
                text_list.append(split_article)
        deconcat_dict.update({site_name: text_list})
    return deconcat_dict
    

def translate_all_text(sites_dict):
    concat_titles_dict = concat_all_text(sites_dict)
    transl_dict = {}
    for site_name in list(sites_dict.keys()):
        transl_dict.update({site_name: translate_word_list(concat_titles_dict[site_name])})
    return transl_dict


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


def find_articles_with_keywords(transl_dict, keyword_list):
    deconcat_dict = deconcat_all_text(transl_dict)
    article_indexes_dict = {}
    list_site_names = list(deconcat_dict.keys())
    for site_name in list_site_names:
        article_list = deconcat_dict[site_name]
        article_indexes_dict.update({site_name: np.zeros((len(article_list), len(keyword_list)))})
        for i_art in range(len(article_list)):
            text = '. '.join(article_list[i_art])
            for j_keyword in range(len(keyword_list)):
                keyword = keyword_list[j_keyword]
                if keyword in text:
                    article_indexes_dict[site_name][i_art, j_keyword] = 1
    return article_indexes_dict


