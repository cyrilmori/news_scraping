from tempfile import NamedTemporaryFile
import webbrowser
import requests
from bs4 import BeautifulSoup
import copy
import unicodedata
import pandas as pd
import regex


MIN_WORDS_IN_TITLE = 5
HIGH_OCCURENCES = 4
MIN_WORD_LEN = 4
PATH_FREQS = ".\\word_frequencies\\"

## Browser visualization

def view_in_browser(html):
    with NamedTemporaryFile("wb", delete=False, suffix=".html") as file:
        file.write(html.encode('utf'))
    webbrowser.open_new_tab(f"file://{file.name}")

def highlight_titles(soup, class_list):
    new_soup = copy.deepcopy(soup)
    for class_str in class_list:
        for tag in new_soup.find_all(class_=class_str):
            strike_tag = new_soup.new_tag('s')
            tag.wrap(strike_tag)
    return new_soup


## Tag selection containing given strings

def count_children(main_tag):
    return len(main_tag.find_all())

def find_childmost_tags(main_tag):
    child_list = []
    for tag in main_tag.find_all():
        if count_children(tag) == 0:
            child_list.append(tag)
    return child_list

def find_childmost_with_text(main_tag):
    child_list = find_childmost_tags(main_tag)
    tags_with_text = []
    for tag in child_list:
        if tag.text != '':
            tags_with_text.append(tag)
    return tags_with_text

def first_parent_with_class(main_tag):
    temp_tag = main_tag
    while temp_tag.has_attr('class') == False:
        temp_tag = temp_tag.parent
    return temp_tag

def get_class_with_string(tags_with_text_list, sample_str, conflict_index=0):
    tag_list = []
    for tag in tags_with_text_list:
        if sample_str in tag.text:
            tag_list.append(tag)
    if len(tag_list) == 0:
        print("Warning: no matches found for the given string: ", sample_str)
        return 0
    elif len(tag_list) > 1:
        print("Warning: several matches with the given string: ", sample_str)
        selected_tag = tag_list[conflict_index]
    else:
        selected_tag = tag_list[0]
    tag_with_class = first_parent_with_class(selected_tag)
    return tag_with_class.attrs['class'][0]

def get_classes_with_strings(tags_with_text_list, string_list, conflict_index=0):
    class_list = []
    for sample_str in string_list:
        class_list.append(get_class_with_string(tags_with_text_list, sample_str, conflict_index=conflict_index))
    return class_list


## Scrape titles from different sites

def get_website_soup(url_str):
    r = requests.get(url_str, auth=('user', 'pass'))
    html_code = r.content.decode('utf')
    soup = BeautifulSoup(html_code, 'html.parser')
    return soup

def format_title_string(str):
    formatted_str = unicodedata.normalize('NFKD', str)
    formatted_str = formatted_str.lower()
    return formatted_str
    
def get_strings_from_class(soup, class_str):
    tags_list = soup.find_all(class_=class_str)
    string_list = []
    for tag in tags_list:
        if len(tag.text.split()) > MIN_WORDS_IN_TITLE:
            string_list.append(format_title_string(tag.text))
    return string_list

def scrape_all_news(list_names, list_url, list_news_classes):
    all_titles_list = []
    for url, class_list in zip(list_url, list_news_classes):
        soup = get_website_soup(url)
        titles_list = []
        for class_str in class_list:
            list_tags = get_strings_from_class(soup, class_str)
            titles_list = titles_list + list_tags
        all_titles_list = all_titles_list + [titles_list]
    return all_titles_list


## Find correlations between texts

def most_common_words(list_texts):
    dict_word_index = {}
    list_freqs = []
    for text, i in zip(list_texts, range(len(list_texts))):
        for word in text.split():
            if not (word in dict_word_index.keys()):
                dict_word_index.update({word: len(list_freqs)})
                list_freqs.append([0]*len(list_texts))
                list_freqs[-1][i] += 1
            else:
                list_freqs[dict_word_index[word]][i] += 1
    return dict_word_index, list_freqs

def filter_keywords(dict_words, list_freqs):
    n_texts = len(list_freqs[0])
    common_words, common_word_freqs = [], []
    for word in list(dict_words.keys()):
        index = dict_words[word]
        frequencies = list_freqs[index]
        count_zeros = 0
        count_highnb = 0
        for f in frequencies:
            if f == 0:
                count_zeros += 1
            if f > HIGH_OCCURENCES:
                count_highnb += 1
        if count_zeros < n_texts-1 and count_highnb == 0:
            common_words.append(word)
            common_word_freqs.append(frequencies)
    return common_words, common_word_freqs

def get_freq_table(lang_str='Fre'):
    file_name = PATH_FREQS + lang_str + '.Freq.3.Hun.txt'
    df = pd.read_csv(file_name, delimiter='\t', index_col='Word')
    return df

def preprocess_word_list(word_list, freq_list):
    processed_words, processed_freqs = [], []
    for word, freq in zip(word_list, freq_list):
        word = word.lower()
        if len(word)>=MIN_WORD_LEN and (regex.fullmatch('\p{Letter}+', word) != None):
            processed_words.append(word)
            processed_freqs.append(freq)
    return processed_words, processed_freqs

def get_word_freqs(freq_df, word_list):
    existing_words = []
    df_index = list(freq_df.index)
    for word in word_list:
        if word in df_index:
            existing_words.append(word)
    return freq_df.loc[existing_words]




