import numpy as np
from datetime import datetime
import os, io, json
from .web_parser import WebParser
from .preprocess import process_data_all_sites
from .compare import flatten_all_sites, get_common_words, get_word_freq_from_lexicon, filter_only_keywords
from .compare_nlp import translate_all_text, filter_keywords_all_sites, find_common_keywords, find_articles_with_keywords, deconcat_all_text


class Interface:
    web_parser = None
    article_dict = {}
    keyword_list = []

    def __init__(self):
        self.web_parser = WebParser('Eng_US')


    #
    # Sites
    #

    def valid_site(self, name):
        return (name in list(self.web_parser.sites_dict.keys()))

    def site_list(self, details=False):
        sites_dict = self.web_parser.sites_dict
        if details:
            print(sites_dict)
        else:
            for name, value in zip(list(sites_dict.keys()), sites_dict.values()):
                print(name + '\t' + value['url'])

    def site_display(self, name):
        if not self.valid_site(name):
            print('Please enter a valid site name.')
            return 0
        self.web_parser.snapshot_site(name)
        self.web_parser.view_in_browser()

    def site_show(self, name):
        if not self.valid_site(name):
            print('Please enter a valid site name.')
            return 0
        sites_dict = self.web_parser.sites_dict
        print(sites_dict[name])

    def site_add(self, url, name='', description='', category=''):
        autoname = self.web_parser.add_site(url, name, description, category)
        if autoname:
            if not name:
                print('Name was automatically set to: ' + autoname)
            print('Site saved successfully.')

    def site_edit(self, name, newname='', description='', category=''):
        if not self.valid_site(name):
            print('Please enter a valid site name.')
            return 0
        if description:
            self.web_parser.update_site(name, 'desc', description)
            print("Description changed to " + description)
        if category:
            self.web_parser.update_site(name, 'category', category)
            print("Category changed to " + category)
        if newname:
            self.web_parser.update_site_name(name, newname)
            print("Name changed to " + newname)
        if not newname and not description and not category:
            print('Please input a new name, description or category in order to edit the chosen site.')
            return 0


    #
    # RSS
    #

    def rss_list(self, site):
        if not self.valid_site(site):
            print('Please enter a valid site name.')
            return 0
        url_list = self.web_parser.sites_dict[site]['rss_urls']
        for i in range(len(url_list)):
            print(str(i) + ':\t' + url_list[i])

    def rss_add(self, site, url, set_desc=False):
        if not self.valid_site(site):
            print('Please enter a valid site name.')
            return 0
        self.web_parser.add_rss(site, url, set_desc)

    def rss_test(self, site, url='', index=None, details=False):
        if not self.valid_site(site):
            print('Please enter a valid site name.')
            return 0
        list_titles, feed_list = self.web_parser.get_rss_site(site, url, index)
        for d in feed_list:
            print(d['title'])
            if details:
                print(d['desc'])

    #
    # Scrape
    #

    def scrape_list(self, site):
        if not self.valid_site(site):
            print('Please enter a valid site name.')
            return 0
        class_list = self.web_parser.sites_dict[site]['scrape_classes']
        for i in range(len(class_list)):
            print(str(i) + ':\t' + class_list[i])

    def scrape_display(self, site, scrape_class, index):
        if not self.valid_site(site):
            print('Please enter a valid site name.')
            return 0
        self.web_parser.snapshot_site(site)
        class_list = self.web_parser.sites_dict[site]['scrape_classes']
        if scrape_class:
            if not scrape_class in class_list:
                print('Note that the given class is not registered for this news site.')
            self.web_parser.highlight_title(scrape_class)
        elif index:
            if 0<=index<range(len(class_list)):
                self.web_parser.highlight_title(class_list[index])
            else:
                print('The class index given is out of bounds.')
                return 0
        else:
            for i in range(len(class_list)):
                self.web_parser.highlight_title(class_list[i])
        self.web_parser.view_in_browser()

    def scrape_test(self, site, scrape_class, index):
        if not self.valid_site(site):
            print('Please enter a valid site name.')
            return 0
        self.web_parser.snapshot_site(site)
        class_list = self.web_parser.sites_dict[site]['scrape_classes']
        if scrape_class:
            if not scrape_class in class_list:
                print('Note that the given class is not registered for this news site.')
            title_list = self.web_parser.get_strings_from_class(scrape_class)
        elif index:
            if 0<=index<range(len(class_list)):
                title_list = self.web_parser.get_strings_from_class(class_list[index])
            else:
                print('The class index given is out of bounds.')
                return 0
        else:
            title_list = self.web_parser.scrape_site(site)
        for entry in title_list:
            print(entry['title'])

    def scrape_add(self, site, scrape_class):
        if not self.valid_site(site):
            print('Please enter a valid site name.')
            return 0
        self.web_parser.add_site_scrape_class(site, scrape_class)

    def scrape_find(self, site, string):
        if not self.valid_site(site):
            print('Please enter a valid site name.')
            return 0
        self.web_parser.snapshot_site(site)
        self.web_parser.print_classes_from_string(string)

    #
    # Keywords
    #

    def keyword_files(self, timeframe=''):
        list_files = os.listdir('.\\saved_keywords\\')
        start, end = None, None
        if timeframe:
            start, end = timeframe.split('_')
            if start:
                start = datetime.strptime(start, '%Y-%m-%d')
            if end:
                end = datetime.strptime(end, '%Y-%m-%d')
        for i in range(len(list_files)):
            flag = True
            file_date_str = list_files[i].split('.')[0]
            file_date = datetime.strptime(file_date_str, '%Y-%m-%d_%H-%M-%S')
            if start and file_date < start:
                flag = False
            if end and file_date > end:
                flag = False
            if flag:
                print(str(i) + ':\t' + list_files[i])

    def keyword_list(self, file_index=None):
        if not file_index:
            file_index = -1
        list_files = os.listdir('.\\saved_keywords\\')
        file_name = list_files[file_index]
        json_file = '.\\saved_keywords\\' + file_name
        with io.open(json_file, 'r', encoding='utf-8') as f:
            loaded_dict = json.load(f)
            keywords = loaded_dict['keywords']
            for i in range(len(keywords)):
                print(str(i) + ':\t' + keywords[i])

    def keyword_get(self, scrape=False):
        rss_dict = self.web_parser.get_all_rss()
        print('Articles scraped.')
        trans_title_dict = translate_all_text(rss_dict)
        print('Articles translated.')
        trans_keywords = filter_keywords_all_sites(trans_title_dict)
        common_keywords = find_common_keywords(trans_keywords)
        keyword_occurences = find_articles_with_keywords(trans_title_dict, common_keywords)
        print('Keywords found.')
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        save_dict = {
            'articles': deconcat_all_text(trans_title_dict),
            'keywords': common_keywords,
            'occurences': {k: v.tolist() for k, v in zip( list(keyword_occurences.keys()), list(keyword_occurences.values()) )}
        }
        json_file = '.\\saved_keywords\\' + timestamp + '.json'
        with io.open(json_file, 'w', encoding='utf-8') as f:
            json.dump(save_dict, f, ensure_ascii=False, indent=4, sort_keys=True)
            print("Keywords saved.")

    def keyword_show(self, keyword, file_index=None, site='', desc=False):
        if not file_index:
            file_index = -1
        list_files = os.listdir('.\\saved_keywords\\')
        file_name = list_files[file_index]
        json_file = '.\\saved_keywords\\' + file_name
        with io.open(json_file, 'r', encoding='utf-8') as f:
            loaded_dict = json.load(f)
            try:
                word_index = loaded_dict['keywords'].index(keyword)
            except:
                print('Not a valid keyword!')
                return 0
            for site in list(loaded_dict['articles']):
                print('\nWEBSITE: ' + site + '\n\n')
                list_articles = loaded_dict['articles'][site]
                list_occurences = np.array(loaded_dict['occurences'][site])[:,word_index]
                for art, freq in zip(list_articles, list_occurences):
                    if freq > 0:
                        for text in art:
                            print(text)
                        print('')

            

