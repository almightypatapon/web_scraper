import requests
import string
import os
from bs4 import BeautifulSoup


def check_url(url):
    try:
        r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        if r.status_code == 200:
            return r
        else:
            print(f'The URL returned {r.status_code}!')
            exit()
    except requests.exceptions.MissingSchema:
        print('Invalid URL!')
        exit()


def get_articles(pages, type_of_article):
    for page_no in range(1, pages + 1):
        articles_saved = []
        r = check_url(r'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={}'.format(page_no))
        soup = BeautifulSoup(r.content, 'html.parser')
        path = r'Page_{}/'.format(page_no)
        os.mkdir(path)
        for article in soup.find_all('article'):
            if article.find('span', {'class': 'c-meta__type'}).text == type_of_article:
                articles = article.find('a', href=True)
                file_name = articles.text.translate(str.maketrans('', '', string.punctuation + '’—')).replace(' ', '_') + '.txt'
                with open(path + file_name, 'w', encoding="utf-8") as file:
                    r = check_url(r'https://www.nature.com' + articles['href'])
                    soup = BeautifulSoup(r.content, 'html.parser')
                    print(soup.find('div', {'class': 'c-article-body u-clearfix'}).text, file=file)
                    articles_saved.append(file_name)
        print(f'Saved articles from page {page_no}:', articles_saved, sep='\n')


get_articles(int(input()), input())
