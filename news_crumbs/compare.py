import numpy as np
import pandas as pd

HIGH_LEXIC_FREQ = 1000
HIGH_OCCURENCES = 4
MIN_WORD_LEN = 4
PATH_FREQS = ".\\word_frequencies\\"


def flatten_site_data(site_list):
    flattened = []
    for item in site_list:
        for text_type in list(item.values()):
            for sentence in text_type:
                flattened += sentence
    return flattened


def flatten_all_sites(sites_dict):
    flattened_dict = {}
    for site_name in list(sites_dict.keys()):
        flattened_dict.update({site_name: flatten_site_data(sites_dict[site_name])})
    return flattened_dict


def create_freq_vector(sites_dict, word_vector):
    n_words = len(word_vector)
    m_sites = len(list(sites_dict.keys()))
    freq_vector = np.zeros((n_words, m_sites))
    return freq_vector


def find_common_words(flat_sites_dict, word_vector):
    freq_vector = create_freq_vector(flat_sites_dict, word_vector)
    for i in range(len(word_vector)):
        for site_name in list(flat_sites_dict.keys()):
            freq_vector[i,:] = np.array([site_data.count(i) for site_data in list(flat_sites_dict.values())])
    return freq_vector


def get_common_words(word_vector, flat_sites_dict):
    freq_vector = find_common_words(flat_sites_dict, word_vector)
    common_words = []
    common_freqs = []
    n, m = freq_vector.shape
    for i in range(n):
        n_matches = np.sum(freq_vector[i,:] != 0)
        if n_matches > 1:
            common_words.append(word_vector[i])
            common_freqs.append(freq_vector[i,:])
    common_freqs = np.array(common_freqs)
    return common_words, common_freqs


def get_word_freq_from_lexicon(lang, word_list, chosen_col='BlogFreq'):
    print('Fetching word frequencies...')
    file_name = PATH_FREQS + lang + '.Freq.3.Hun.txt'
    freq_df = pd.read_csv(file_name, delimiter='\t', index_col='Word', usecols=['Word', chosen_col])
    word_freq_list = []
    for word in word_list:
        if word in list(freq_df.index):
            word_freq_list.append(int(freq_df.loc[word][chosen_col]))
        else:
            word_freq_list.append(-1)
    return word_freq_list


def filter_only_keywords(word_list, lexic_freq_list, sites_freq):
    keyword_list = []
    for word, freq, site_f_vec in zip(word_list, lexic_freq_list, sites_freq):
        if len(word) >= MIN_WORD_LEN and \
                freq < HIGH_LEXIC_FREQ and \
                sum([f < HIGH_OCCURENCES for f in site_f_vec]):
            keyword_list.append(word)
    return keyword_list
