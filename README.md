# NewsCrumbs

A CLI tool for scraping and gathering RSS fluxes from various news websites and then searching for common keywords using NLP. It includes a translation function for non-English websites.

**Table of contents:**
- [List of commands](#list-of-commands)
    - [News websites](#news-websites)
    - [RSS fluxes](#rss-fluxes)
    - [Scraping classes](#scraping-classes)
    - [Retrieved keywords](#retrieved-keywords)
- [Future improvements](#future-improvements)


# List of commands

General format for the commands:
```
newscrumbs [object] [action] [[arguments]]
```
Each subcategory of commands below details available actions for a given typo of object. Note that optional arguments of the form ```--argument``` always have a shorthand version using their initial, such as ```-a```.


## News websites

Commands for managing and editing registered news websites.
Format for the commands:
```
newscrumbs site [action] [[arguments]]
```
**Actions:**
- Make a list of all registered website. Using the keyword ```--details``` shows the full dictionary of websites with all their parameters, otherwise only the site names and URLs are shown.
```
newscrumbs site list --details
```
- Display the website identified by ```[name]``` in web browser. 
```
newscrumbs site display [name]
```
- Show the registered properties for the website identified by ```[name]```.
```
newscrumbs site show [name]
```
- Add the website identified by ```[url]``` to the saved database. Optional arguments ```--name```, ```--description``` and ```--category``` can be added to set the site's properties. If not specified, the saved site's name is automatically set using the URL.
```
newscrumbs site add [url] --name --description --category (display autoname)
```
- Edit the properties for the website identified by ```[name]```.
```
newscrumbs site edit name --newname --description --category
```


## RSS fluxes

Commands for managing and editing registered RSS fluxes.
Format for the commands:
```
newscrumbs rss [action] [[arguments]]
```
**Actions:**
- Print all the RSS URLs registered for the website named ```[site]```. Also prints their corresponding indices in the list.
```
newscrumbs rss list [site]
```
- Add an RSS flux with the URL ```[url]``` for the website named ```[site]```. Setting the argument ```--description``` will use the RSS flux to automatically set the saved description property of the website.
```
newscrumbs rss add [site] [url] --description
```
- Test the RSS fluxes of the website named ```[site]``` by retrieving and printing their data. In order to test a single RSS flux, it can be identified through the optional arguments ```--url``` or ```--index``` (index of the RSS flux when listing them).
```
newscrumbs rss test [site] --url --index
```


## Scraping classes

Commands for managing and editing tag classes used for scraping websites. The actions ```find```, ```test``` and ```display``` are used for finding tags associated to specific text and to test their scraping. 
Format for the commands:
```
newscrumbs scrape [action] [[arguments]]
```
**Actions:**
- List all the registered tag classes for scraping the website named ```[site]```. Also prints their corresponding indices in the list.
```
newscrumbs scrape list [site]
```
- Add the class string ```[scrapeclass]``` for the website named ```[site]```.
```
newscrumbs scrape add [site] [scrapeclass]
```
- Test the classes registered to scrape the website named ```[site]``` by retriving their associated data and printing it. In order to test a single class, it can be identified by its string ```--scrapeclass``` or by its index in the list ```--index```.
```
newscrumbs scrape test [site] --scrapeclass --index
```
- Display the site named ```[site]``` in the web browser and indicate text to be scraped by ~~striking~~ it. In order to test a single tag class for the website, it can be identified by its string ```--scrapeclass``` or its index in the list ```--index```.
```
newscrumbs scrape display [site] --scrapeclass --index
```
- Searches the website named ```[site]``` for the text ```[string]``` and prints possible classes which could be associated to this text. Note that only classes containing a single block of text are printed.
```
newscrumbs scrape find [site] [string]
```


## Retrieved keywords

Commands for retrieving news data, identifying common keywords and and saving them to local json files.
Format for the commands:
```
newscrumbs keyword [action] [[arguments]]
```
**Actions:**
- Retrieve all news data and identify common keywords then save all the data to a timestamped json file. The optional argument ```--scrape``` can be used to use scraped data instead of just RSS fluxes.
```
newscrumbs keyword get --scrape
```
- Print a list of previously saved news data files with their names and indices. Optional argument ```--date``` can be used to set a date bracket with the format "YYYY-mm-dd_YYYY-mm-dd". If one of the dates is omitted, it is counted as an open bracket.
```
newscrumbs keyword files --date
```
- List all the saved keywords for the registered file identified by its index ```--file```. If no index is given, the last saved file is used by default.
```
newscrumbs keyword list --file
```
- Print all saved articles containing the word ```[keyword]``` in the file identified by its index ```--file```. If no index is given, the last saved file is used by default. A single website can be used by identifying it with its name ```--site```. Optional argument ```--description``` is used to display articles' descriptions instead of only titles.
```
newscrumbs keyword show [keyword] --file --site --description
```


# Future improvements

- Move all printing to the interface instead of webparser
- Move all safety testing (eg site name) to webparser
- Implement saving keywords
- Take out languages setting from webparser
- Allow testing of rss url without any site argument
- Implement keyword search including data from scraped classes
- Truncate articles list when there's too many
- Raise errors instead of jsut printing
- Stop accounting for character case in find_common_keywords()
- Make blacklisted keywords ('image', 'live', etc)
- Add progress bars for scraping and translating
- Implement list of tags functionality
