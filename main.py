from news_crumbs.web_parser import WebParser
from news_crumbs.preprocess import process_data_all_sites
from news_crumbs.compare import flatten_all_sites, get_common_words, get_word_freq_from_lexicon, filter_only_keywords
from news_crumbs.compare_nlp import translate_word_list, filter_keywords_nlp



#
# Scrape the news
#

parser = WebParser('Fre')

## Add website
parser.add_site(
    url = 'https://www.france24.com/fr/',
    desc = '',
    rss_list = [
        'https://www.france24.com/fr/rss',
    ],
    scrape_list = []
) 
# parser.add_rss('lemonde', 'https://www.lemonde.fr/international/rss_full.xml')

# ## Scraping
# parser.snapshot_site('mediapart')
# parser.view_in_browser()
# parser.print_classes_from_string('Laurence des Cars')
# parser.highlight_title('article__title')
# # parser.view_in_browser()
# parser.add_site_scrape_class('lemonde', 'article__title')
# scraped_titles = parser.scrape_all_news()['lemonde']

## RSS feed
rss_dict = parser.get_all_rss()




#
# Pre-process the data
#

processed_dict, vector = process_data_all_sites(rss_dict)




#
# Compare data between sites
#

flat_dict = flatten_all_sites(processed_dict)
common_words, common_freqs = get_common_words(vector, flat_dict)
lexic_freq = get_word_freq_from_lexicon('Fre', common_words)
keywords = filter_only_keywords(common_words, lexic_freq, common_freqs)
# print(keywords)




#
# NLP version in English
#

trans_word_list = translate_word_list(keywords)
trans_keywords = filter_keywords_nlp(trans_word_list)
print(trans_keywords)

