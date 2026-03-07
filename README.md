# NewsCrumbs


This is a CLI tool for scraping and gathering RSS fluxes from various news websites and then searching for common keywords using NLP. It includes a translation function for non-English websites.


## List of commands

General format for the commands:
```
newscrumbs [object] [action] [[arguments]]
```
Each subcategory of commands below details available actions for a given typo of object.


## News websites

Commands for managing and editing registered news websites.
Format for the commands:
```
newscrumbs site [action] [[arguments]]
```
**Actions:**
- list --details
- display [name]
- show [name]
- add [url] --name --description --category (display autoname)
- edit name --newname --description --category


## RSS fluxes

Commands for managing and editing registered news websites.
Format for the commands:
```
newscrumbs rss [action] [[arguments]]
```
**Actions:**
- list [site]
- add [site] [rss_url] --setdesc
- test [site] --url --index


## Scraping classes

Commands for managing and editing registered news websites.
Format for the commands:
```
newscrumbs scrape [action] [[arguments]]
```
**Actions:**
- list [site]
- add [site] [scrapeclass]
- test [site] --scrapeclass --index
- display [site] --scrapeclass --index
- find [site] [string]


## Retrieved keywords

Commands for managing and editing registered news websites.
Format for the commands:
```
newscrumbs keyword [action] [[arguments]]
```
**Actions:**
- get --scrape (scrape and save news from all sites then find common keywords and show them)
- list (lists all keywords registered)


## Improvements to make

- move all printing to the interface instead of webparser
- move all safety testing (eg site name) to webparser
- implement saving keywords
- take out languages setting from webparser
- allow testing of rss url without any site argument
- implement keyword search including data from scraped classes
- truncate articles list when there's too many (eg chinadaily)
- raise errors instead of jsut printing
- stop accounting for character case in find_common_keywords()
- make blacklisted keywords ('image', 'live', etc)
- add progress bars for scraping and translating
- implement list of tags functionality
