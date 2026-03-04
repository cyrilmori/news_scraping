import argparse


'''
LIST OF FUNCTIONALITIES:
newscrumbs
    site
        list --details
        display [name]
        show [name]
        add [url] --name --desc --category (display autoname)
        edit --name --desc --category
    rss
        list [site]
        add [site] [rss_url]
        test [site] --url --index
    scrape
        list [site]
        add [site] [scrape_class]
        test --class --index
        display --class --index
        find [site] [string]
    keywords
        get --scrape (scrape and save news from all sites then find common keywords and show them)
        list (lists all keywords registered)
        show [keyword] --site --description (shows articles associated to keyword)
'''


def main(command_line=None):
    parser = argparse.ArgumentParser(
        prog='News Crumbs',
        description='A scraper that takes in RSS feed data from registered websites and finds the most mentioned keywords.'
    )
    subparsers = parser.add_subparsers(dest='object')

    #
    # Site management
    #
    site = subparsers.add_parser(
        'site',
        help = 'Manage registered news websites in the database.'
    )
    site_subparsers = site.add_subparsers(dest='action')

    # list
    site_list = site_subparsers.add_parser(
        'list',
        help = 'List all registered websites.'
    )
    site_list.add_argument('-d', '--details', action='store_true', help = 'Show full details for each site instead of just title and URL.')
    
    # display
    site_display = site_subparsers.add_parser(
        'display',
        help = 'Display a given website in browser.'
    )
    site_display.add_argument('name', type=str, help = 'Name of the website to be displayed.')
    
    # show
    site_show = site_subparsers.add_parser(
        'show',
        help = 'Show all registered parameters of a given website.'
    )
    site_show.add_argument('name', type=str, help = 'Name of the website to be shown.')

    # add
    site_add = site_subparsers.add_parser(
        'add',
        help = 'Add a website.'
    )
    site_add.add_argument('url', type=str, help = 'URL of the website to be added.')
    site_add.add_argument('-n', '--name', type=str, help = 'Name of the website to be added.')
    site_add.add_argument('-d', '--descrition', type=str, help = 'Description of the website to be added.')
    site_add.add_argument('-c', '--category', type=str, help = 'Category of the website to be added.')

    # edit
    site_edit = site_subparsers.add_parser(
        'edit',
        help = 'Edit name/description/category of a registered website. Use subcommands rss and scrape to modify the scraping parameters.',
    )
    site_edit.add_argument('name', help = 'Name of the website to be edited.')
    site_edit.add_argument('-n', '--newname', type=str, help = 'New name of the website.')
    site_edit.add_argument('-d', '--descrition', type=str, help = 'New description of the website.')
    site_edit.add_argument('-c', '--category', type=str, help = 'New category of the website.')



    #
    # RSS flux management
    #
    rss = subparsers.add_parser(
        'rss',
        help = 'Manage registered RSS fluxes in the database.'
    )
    rss_subparsers = rss.add_subparsers(dest='action')

    # list
    rss_list = rss_subparsers.add_parser(
        'list',
        help = 'List all registered RSS fluxes and their indices for a given news site.'
    )
    rss_list.add_argument('site', type=str, help = 'Name of the chosen website.')

    # add
    rss_add = rss_subparsers.add_parser(
        'add',
        help = 'Add an RSS flux to a chosen website.'
    )
    rss_add.add_argument('site', type=str, help = 'Name of the chosen website.')
    rss_add.add_argument('url', type=str, help = 'URL of the RSS flux to be added.')

    # test
    rss_test = rss_subparsers.add_parser(
        'test',
        help = 'Test RSS flux for a given website.'
    )
    rss_test.add_argument('site', type=str, help = 'Name of the chosen website.')
    rss_test.add_argument('-i', '--index', type=str, help = 'Index of the RSS if a single one is to be tested.')


    #
    # Scraping classes management
    #
    scrape = subparsers.add_parser(
        'scrape',
        help = 'Manage classes used for identifying the tags to scrape.'
    )
    scrape_subparsers = scrape.add_subparsers(dest='action')

    # list
    scrape_list = scrape_subparsers.add_parser(
        'list',
        help = 'List all registered scrape classes and their indices for a given news site.'
    )
    scrape_list.add_argument('site', type=str, help = 'Name of the chosen website.')

    # add
    scrape_add = scrape_subparsers.add_parser(
        'add',
        help = 'Add an scrape flux to a chosen website.'
    )
    scrape_add.add_argument('site', type=str, help = 'Name of the chosen website.')
    scrape_add.add_argument('class', type=str, help = 'Class name for the tags to be scraped.')

    # test
    scrape_test = scrape_subparsers.add_parser(
        'test',
        help = 'Test scrape flux for a given website.'
    )
    scrape_test.add_argument('site', type=str, help = 'Name of the chosen website.')
    scrape_test.add_argument('-c', '--class', type=str, help = 'Class name if a single one is to be tested.')
    scrape_test.add_argument('-i', '--index', type=str, help = 'Index of the class if a single one is to be tested.')

    # display
    scrape_display = scrape_subparsers.add_parser(
        'display',
        help = 'Display the chosen website in browser and strike all text scraped by the registered classes.'
    )
    scrape_display.add_argument('site', type=str, help = 'Name of the chosen website.')
    scrape_display.add_argument('-c', '--class', type=str, help = 'Class name if a single one is to be scraped.')
    scrape_display.add_argument('-i', '--index', type=str, help = 'Index of the class if a single one is to be scraped.')

    # find
    scrape_find = scrape_subparsers.add_parser(
        'find',
        help = 'Find all tag classes related to a sample string in the chosen website.'
    )
    scrape_find.add_argument('site', type=str, help = 'Name of the chosen website.')
    scrape_find.add_argument('string', type=str, help = 'Sample text used for locating the classes of tags to be scraped.')



    #
    # Keywords management
    #
    keyword = subparsers.add_parser(
        'keyword',
        help = 'Scrape news and organize them by common keywords.'
    )
    keyword_subparsers = keyword.add_subparsers(dest='action')

    # get
    keyword_get = keyword_subparsers.add_parser(
        'get',
        help = 'Get all news data, save it to RAM then identify common keywords.'
    )
    keyword_get.add_argument('-s', '--scrape', type=str, help = 'Also scrape titles using registered classes instead of relying only on RSS fluxes.')
    # keyword_get.add_argument('-w', '--write', type=str, help = 'Save all scraped data to a text file.')

    # list
    keyword_list = keyword_subparsers.add_parser(
        'list',
        help = 'List all registered keywords.'
    )

    # show
    keyword_show = keyword_subparsers.add_parser(
        'show',
        help = 'show keyword flux for a given website.'
    )
    keyword_show.add_argument('keyword', type=str, help = 'Keyword used to filter which articles are shown.')
    keyword_show.add_argument('-s', '--site', type=str, help = 'Name of the chosen website if a single one is to be shown.')
    keyword_show.add_argument('-d', '--description', type=str, help = 'Print also articles\' descriptions instead of just titles.')



    args = parser.parse_args(command_line)



if __name__ == '__main__':
    main()

