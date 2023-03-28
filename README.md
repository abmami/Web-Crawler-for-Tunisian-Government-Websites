Web Crawler for Tunisian Government Websites
==============================

This repository contains a web crawler designed to extract sub URLs from a list of 20 Tunisian government websites, and then scrape their contents to construct a small dataset of web pages that could possibly be used for natural language processing tasks.


### Run Locally

If you want to re-run the crawling process, follow these steps: 

* Install the required Python packages using pip:
```bash
  pip install -r requirements.txt
```
* Update the urls.txt file with a list of Tunisian government website URLs you wish to crawl.
* Run crawler.py to start the web crawler.
```bash
  python crawler.py
```
The URLs that were successfully extracted from the websites can be found in the "/data/urls.json" file. 
The contents of each URL are stored in the "/data/content.json" file.  
*  Process the raw contents using spaCy to extract and filter sentences.
```bash
  python clean.py
```
The fileterd contents of each URL are stored in the "/data/filtered_content.json" file.

