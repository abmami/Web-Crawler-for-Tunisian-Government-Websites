import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from warnings import filterwarnings
filterwarnings('ignore')

def crawl_websites(urls, keywords, allowed_domains):
    # initialize list to hold crawled urls
    all_urls = []
    with tqdm(total=len(urls)) as pbar:
        # loop through each url in the urls list
        for url in urls:
            try:
                # send request to url
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                response = requests.get(url, headers=headers, timeout=5, allow_redirects=True, verify=False)

                # check response status code, and content type
                if response.status_code != 200 or 'text/html' not in response.headers.get('Content-Type'):
                    continue

                # parse html content using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # find all links on page
                links = soup.find_all('a')

                # loop through each link
                for link in links:
                    href = link.get('href')

                    # check if link matches any of the base urls
                    if "http" not in href:
                        # remove '/' from the start of the url and url has '/' at the end
                        if href.startswith('/') and url.endswith('/'):
                            href = href[1:]
                        href = url + href

                    # filter out urls with keywords
                    if any(keyword in href for keyword in keywords):
                        continue

                    # filter out urls with domains
                    if not any(domain in href for domain in allowed_domains):
                        continue
                    all_urls.append(href.strip())

            except Exception as e:
                print(f'Error crawling {url}: {e}')
            pbar.update(1)

    # remove duplicates
    all_urls = list(set(all_urls))
    
    # save crawled urls 
    with open('./data/urls.json', 'w', encoding='utf-8') as f:
        json.dump(all_urls, f, indent=4, ensure_ascii=False)
        print(len(all_urls), 'urls saved to ./data/urls.json')

    return all_urls

def crawl_url(url):
    # sent request to url
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True, verify=False)

        # check response status code, and content type
        if response.status_code != 200 or 'text/html' not in response.headers.get('Content-Type'):
            return "Error"
    
        # parse html content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find('body')

        # return the content of the url
        return body.text
    except Exception as e:
        print(f'Error crawling {url}: {e}')
        return "Error"

if __name__ == '__main__':
    # read urls from the txt file
    with open('./data/websites.txt') as f:
        urls = f.read().splitlines()


    # keywords to filter out
    keywords = ['mailto', 'facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'pinterest', 'tumblr', 'flickr', 'vimeo', 'dribbble', 'behance', 'github', 'bitb']

    # allowed domains to keep
    allowed_domains = ['.tn', '.gov.tn']

    # crawl websites
    all_urls = crawl_websites(urls, keywords, allowed_domains)

    # crawl urls content 
    content = {}
    with tqdm(total=len(all_urls)) as pbar:
        for url in all_urls:
            content[url] = crawl_url(url)
            pbar.update(1)
            
    # save content of the crawled urls
    with open('./data/content.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)
        print(len(content), 'contents saved to ./data/content.json')

