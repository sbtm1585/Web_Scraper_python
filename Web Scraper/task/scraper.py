import requests
from bs4 import BeautifulSoup
import string
import os


def scraper(url, n, article_type):
    headers = {'Accept-Language': 'en-US,en;q=0.5'}
    for i in range(1, n+1):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')
        article_links = []
        for article in articles:
            if article.find('span', {'data-test': 'article.type'}).text == article_type:
                article_links.append("https://www.nature.com"
                     + article.find('a', {'data-track-action': 'view article'})['href'])
        article_dict = get_body(article_links)
        write_files(article_dict, i)
        url = "https://www.nature.com" + new_url(url, soup)
    print("Saved all articles.")


def get_body(article_links):
    article_dict = {}
    for link in article_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').text
        title = title.strip(string.punctuation).replace(" ","_").strip()
        teaser_text = soup.find('p', {'class': 'article__teaser'})
        if teaser_text is None:  # if teaser text is None get alternative teaser
            main_article = soup.find('div', {'class': 'c-article-body main-content'})
            teaser_text = main_article.find('p').text.strip().encode('utf-8')
        else:
            teaser_text = teaser_text.text.strip().encode('utf-8')
        article_dict[title] = teaser_text
    return article_dict


def write_files(article_dict, i):
    saved_articles = []
    new_dir = make_new_dir(i)
    for title, teaser in article_dict.items():
        if teaser is not None:
            with open(f"{new_dir}/{title}.txt", "wb") as file:
                file.write(teaser)
            saved_articles.append(title)
        else:
            pass
    if len(saved_articles) > 0:
        print(f"Saved articles from page {i}:", saved_articles)
    else:
        print(f"No articles found on page {i}.")


def make_new_dir(i):
    new_dir = f"{os.getcwd()}/Page_{i}"
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    return new_dir


def new_url(url, soup):
    new_url_list = soup.find_all('a', {'class': 'c-pagination__link'})
    for item in new_url_list:
        text = item.find('span').text
        if text == "Next page":
            new_url = item['href']
    return new_url


if __name__ == '__main__':
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
    n = int(input())
    article_type = input()
    scraper(url, n, article_type)
