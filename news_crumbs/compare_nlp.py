import numpy as np
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
    print('Translating word list...')
    sentence = '.'.join(word_list)
    translated = GoogleTranslator(source='auto', target='en').translate(sentence)
    return translated.split('.')


def filter_keywords_nlp(word_list):
    print('Searching for keywords...')
    for word in word_list:
        try:
            tokens = nltk.word_tokenize(word)
            tagged = nltk.pos_tag(tokens)
            filtered_list = []
            for tag in tagged:
                if tag[1] in ['NN', 'NNP', 'NNPS', 'NNS']:
                    filtered_list.append(tag[0])
        except:
            print('Word "'+word+'" not found')
    return filtered_list


