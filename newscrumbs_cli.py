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
        test [site] --rss_url
    scrape
        list
        display --class_name (highlights)
        test --class_name
        find [string] (returns possible classes)
    keywords
        update (scrape all sites and find common keywords then show them)
        show [keyword] --content (shows articles associated to keyword)
        list (shows all keywords registered)
'''


def main(command_line=None):
    parser = argparse.ArgumentParser(
        prog='News Crumbs',
        description='A scraper that takes in RSS feed data from registered websites and finds for the most mentioned keywords.'
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
    site_list = subparsers.add_parser(
        'list',
        help = 'List all registered websites.'
    )
    site_list.add_argument('-d', '--details', type=bool, help = 'Show full details for each site instead of just title and URL.')
    
    # display
    site_display = subparsers.add_parser(
        'display',
        help = 'Display a given website in browser.'
    )
    site_display.add_argument('name', type=str, help = 'Name of the website to be displayed.')
    
    # show
    site_show = subparsers.add_parser(
        'show',
        help = 'Show all registered parameters of a given website.'
    )
    site_show.add_argument('name', type=str, help = 'Name of the website to be shown.')

    # add
    site_add = subparsers.add_parser(
        'add',
        help = 'Add a website.'
    )
    site_add.add_argument('url', type=str, help = 'URL of the website to be added.')
    site_add.add_argument('-n', '--name', type=str, help = 'Name of the website to be displayed.')
    site_add.add_argument('-d', '--descrition', type=str, help = 'Description of the website to be displayed.')
    site_add.add_argument('-c', '--category', type=str, help = 'Category of the website to be displayed.')

    # edit
    site_edit = subparsers.add_parser(
        'edit',
        help = 'Edit name/description/category of a registered website. Use subcommands rss and scrape to modify the scraping parameters.',
    )
    site_edit.add_argument('name', help = 'Name of the website to be edited.')
    site_edit.add_argument('-n', '--newname', type=str, help = 'New name of the website to be displayed.')
    site_edit.add_argument('-d', '--descrition', type=str, help = 'New description of the website to be displayed.')
    site_edit.add_argument('-c', '--category', type=str, help = 'New category of the website to be displayed.')

    args = parser.parse_args(command_line)



if __name__ == '__main__':
    main()