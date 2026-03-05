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
    scraped_dict = {}
    rss_feeds_dict = {}
    
    
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
        else:
            self.read_json()
    

    #
    # Manage dictionary and json file
    #

    def save_json(self):
        with io.open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.sites_dict, f, ensure_ascii=False, indent=4, sort_keys=True)


    def read_json(self):
        with io.open(self.json_file, 'r', encoding='utf-8') as f:
            self.sites_dict = json.load(f)


    def add_site(self, url, site_name='', desc='', category='', rss_list=[], scrape_list=[], auto_save=True):
        if not site_name:
            site_name = url.split('.')[1]
        if not (site_name in list(self.sites_dict.keys())):
            self.sites_dict.update({
                site_name: {
                    'url': url,
                    'desc': desc,
                    'rss_urls': rss_list,
                    'scrape_classes': scrape_list,
                    'category': category,
                }
            })
            if auto_save:
                self.save_json()
            return site_name
        else:
            print('Site is already saved, call update_site() instead.')
            return 0
    

    def update_site_name(self, name, newname, auto_save=True):
        self.sites_dict[newname] = self.sites_dict[name]
        del self.sites_dict[name]
        if auto_save:
            self.save_json()


    def update_site(self, name, key, value, auto_save=True):
        self.sites_dict[name][key] = value
        if auto_save:
            self.save_json()
    

    def add_site_scrape_class(self, site_name, class_name, auto_save=True):
        if site_name in list(self.sites_dict.keys()):
            if not class_name in self.sites_dict[site_name]['scrape_classes']:
                self.sites_dict[site_name]['scrape_classes'].append(class_name)
            else:
                print('Class is already saved.')
            if auto_save:
                self.save_json()
        else:
            print('Site name not registered!')
    

    def add_rss(self, site_name, rss_url, change_desc=False):
        if site_name in list(self.sites_dict.keys()):
            if change_desc:
                d = feedparser.parse(rss_url)
                self.update_site(site_name, 'desc', d.feed.title)
            if rss_url in self.sites_dict[site_name]['rss_urls']:
                print('RSS URL is already saved.')
            else:
                self.sites_dict[site_name]['rss_urls'].append(rss_url)
                self.save_json()
                print('RSS url successfully added.')
        else:
            print('Site name not registered!')


    #
    # Snapshot a website for testing scraping
    #
    
    def snapshot_site(self, site_name):
        # Take a snapshot of a website to test the scraping
        url_str = self.sites_dict[site_name]['url']
        r = requests.get(url_str, auth=('user', 'pass'))
        html_code = r.content.decode('utf')
        self.snapshot_soup = BeautifulSoup(html_code, 'html.parser')


    def view_in_browser(self):
        html = str(self.snapshot_soup)
        with NamedTemporaryFile("wb", delete=False, suffix=".html") as file:
            file.write(html.encode('utf'))
        webbrowser.open(f"file://{file.name}")


    def highlight_title(self, class_str):
        new_soup = copy.deepcopy(self.snapshot_soup)
        for tag in new_soup.find_all(class_=class_str):
            strike_tag = new_soup.new_tag('s')
            tag.wrap(strike_tag)
        self.snapshot_soup = new_soup


    #
    # Tag selection containing given strings
    #

    def count_children(self, main_tag):
        return len(main_tag.find_all())


    def find_childmost_with_text(self, main_tag):
        child_list = []
        for tag in main_tag.find_all():
            if self.count_children(tag) == 0 and tag.text != '':
                child_list.append(tag)
        return child_list


    def print_parents_with_class(self, main_tag):
        temp_tag = main_tag
        while temp_tag.text == main_tag.text:
            if temp_tag.has_attr('class'):
                print(temp_tag.attrs['class'])
            temp_tag = temp_tag.parent


    def print_classes_from_string(self, sample_str):
        n_matches = 0
        tags_with_text_list = self.find_childmost_with_text(self.snapshot_soup)
        for tag in tags_with_text_list:
            if sample_str in tag.text:
                self.print_parents_with_class(tag)
                n_matches += 1
        if n_matches == 0:
            print("Warning: no matches found for the given string: ", sample_str)
            return 0
        elif n_matches > 1:
            print("Warning: ", str(n_matches), " matches with the given string: ", sample_str)


    def get_strings_from_class(self, class_str):
        tags_list = self.snapshot_soup.find_all(class_=class_str)
        return [{'title': tag.text} for tag in tags_list]
    

    def scrape_site(self, site_name):
        self.snapshot_site(site_name)
        titles_list = []
        for class_str in self.sites_dict[site_name]['scrape_classes']:
            titles_list = titles_list + self.get_strings_from_class(class_str)
        return titles_list


    def scrape_all_news(self):
        titles_dict = {}
        for site_name in list(self.sites_dict.keys()):
            titles_list = self.scrape_site(site_name, titles_dict)
            titles_dict.update({site_name: titles_list})
        self.scraped_dict = titles_dict
        return titles_dict
    

    #
    # RSS feeds
    #

    def get_rss(self, url, list_titles=[], feed_list=[]):
        d = feedparser.parse(url)
        for entry in d.entries:
            if not entry.title in list_titles:
                feed_list = feed_list + [{
                    'title': entry.title,
                    'desc': entry.description,
                }]
                list_titles.append(entry.title)
        return list_titles, feed_list


    def get_rss_site(self, site_name, url='', index=None):
        rss_urls = self.sites_dict[site_name]['rss_urls']
        list_titles = []
        feed_list = []
        if url:
            if not url in rss_urls:
                print('Note that the given URL is not registered for this news site.')
            list_titles, feed_list = self.get_rss(url, list_titles, feed_list)
        elif index:
            if 0<=index<len(rss_urls):
                url = rss_urls[index]
                list_titles, feed_list = self.get_rss(self, url, list_titles, feed_list)
            else:
                print('The URL index given is out of bounds.')
                return 0
        else:
            for url in rss_urls:
                list_titles, feed_list = self.get_rss(url, list_titles, feed_list)
        return list_titles, feed_list
    
    
    def get_all_rss(self):
        rss_dict = {}
        for site_name in list(self.sites_dict.keys()):
            feed_list = self.get_rss(site_name)
            rss_dict.update({site_name: feed_list})
        return rss_dict
