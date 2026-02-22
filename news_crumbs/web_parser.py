import io, os, json
import webbrowser
import copy
from tempfile import NamedTemporaryFile
import requests
from bs4 import BeautifulSoup
import feedparser

AVAILABLE_LANGS = [
    'Fre',
    'Eng_US',
]

class WebParser:
    '''
        Class that loads all news sites and scrapes/reads RSS from them to return news content.
    '''

    lang = ''
    json_file = ''
    sites_dict = {}
    snapshot_soup = None
    
    def __init__(self, lang):
        self.available_langs = [file.split('.')[0] for file in os.listdir('.\\word_frequencies\\')]
        if lang in self.available_langs:
            self.lang = lang
        else:
            raise ValueError('Not a valid language string!')
        
        # Initialize website dictionary and create json file if necessary
        self.json_file = '.\\websites_config\\' + lang + '.json'
        if not os.path.exists(self.json_file):
            self.sites_dict = {}
            self.save_json()
            print('No websites registered yet.')
        else:
            self.read_json()
            print('The following websites are registered: ', *list(self.sites_dict.keys()))
    

    #
    # Manage dictionary and json file
    #

    def save_json(self):
        with io.open(self.json_file, 'a', encoding='utf-8') as f:
            json.dumps(self.sites_dict, f, ensure_ascii=False, indent=4, sort_keys=True)


    def read_json(self):
        with io.open(self.json_file, 'a', encoding='utf-8') as f:
            self.sites_dict = json.load(f)


    def add_site(self, url, desc='', rss_list=[], scrape_list=[], auto_save=True):
        site_name = url.split('.')[1]
        self.sites_dict.update({
            site_name: {
                'url': url,
                'desc': desc,
                'rss_urls': rss_list,
                'scrape_classes': scrape_list,
            }
        })
        if auto_save:
            self.save_json()
    

    def update_site(self, name, key, value, auto_save=True):
        self.sites_dict[name][key] = value
        if auto_save:
            self.save_json()


    #
    # Snapshot a website for testing scraping
    #
    
    def snapshot_site(self, site_name):
        # Take a snapshot of a website to test the scraping
        url_str = self.sites_dict[site_name]
        r = requests.get(url_str, auth=('user', 'pass'))
        html_code = r.content.decode('utf')
        self.snapshot_soup = BeautifulSoup(html_code, 'html.parser')


    def view_in_browser(self):
        html = str(self.snapshot_soup)
        with NamedTemporaryFile("wb", delete=False, suffix=".html") as file:
            file.write(html)
        webbrowser.open_new_tab(f"file://{file.name}")


    def highlight_titles(self, class_list):
        new_soup = copy.deepcopy(self.snapshot_soup)
        for class_str in class_list:
            for tag in new_soup.find_all(class_=class_str):
                strike_tag = new_soup.new_tag('s')
                tag.wrap(strike_tag)
        return new_soup


# ## Tag selection containing given strings

# def count_children(main_tag):
#     return len(main_tag.find_all())

# def find_childmost_tags(main_tag):
#     child_list = []
#     for tag in main_tag.find_all():
#         if count_children(tag) == 0:
#             child_list.append(tag)
#     return child_list

# def find_childmost_with_text(main_tag):
#     child_list = find_childmost_tags(main_tag)
#     tags_with_text = []
#     for tag in child_list:
#         if tag.text != '':
#             tags_with_text.append(tag)
#     return tags_with_text

# def first_parent_with_class(main_tag):
#     temp_tag = main_tag
#     while temp_tag.has_attr('class') == False:
#         temp_tag = temp_tag.parent
#     return temp_tag

# def get_class_with_string(tags_with_text_list, sample_str, conflict_index=0):
#     tag_list = []
#     for tag in tags_with_text_list:
#         if sample_str in tag.text:
#             tag_list.append(tag)
#     if len(tag_list) == 0:
#         print("Warning: no matches found for the given string: ", sample_str)
#         return 0
#     elif len(tag_list) > 1:
#         print("Warning: several matches with the given string: ", sample_str)
#         selected_tag = tag_list[conflict_index]
#     else:
#         selected_tag = tag_list[0]
#     tag_with_class = first_parent_with_class(selected_tag)
#     return tag_with_class.attrs['class'][0]

# def get_classes_with_strings(tags_with_text_list, string_list, conflict_index=0):
#     class_list = []
#     for sample_str in string_list:
#         class_list.append(get_class_with_string(tags_with_text_list, sample_str, conflict_index=conflict_index))
#     return class_list


# ## Scrape titles from different sites


# def get_strings_from_class(soup, class_str):
#     tags_list = soup.find_all(class_=class_str)
#     string_list = []
#     for tag in tags_list:
#         if len(tag.text.split()) > MIN_WORDS_IN_TITLE:
#             string_list.append(format_title_string(tag.text))
#     return string_list

# def scrape_all_news(list_names, list_url, list_news_classes):
#     all_titles_list = []
#     for url, class_list in zip(list_url, list_news_classes):
#         soup = get_website_soup(url)
#         titles_list = []
#         for class_str in class_list:
#             list_tags = get_strings_from_class(soup, class_str)
#             titles_list = titles_list + list_tags
#         all_titles_list = all_titles_list + [titles_list]
#     return all_titles_list

