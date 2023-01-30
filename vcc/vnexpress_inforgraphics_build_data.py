import json
import random
import time
from pathlib import Path

import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm

from vcc.image_caption import ImageCaption


DATA_DIR = Path(r"data/vnexpress/inforgraphics")
START_INDEX = 1
END_INDEX = 18


def make_article_list():
    article_list = []
    http = urllib3.PoolManager()
    for i in tqdm(range(START_INDEX, END_INDEX+1)):
        time.sleep(random.randint(1, 3))  # Slow down so server might think this is a human
        inforgraphics_page = f"https://vnexpress.net/infographics-p{i}"
        response = http.request('GET', inforgraphics_page)
        soup = BeautifulSoup(response.data, 'lxml')
        articles_field = soup.find('div', class_="col-left-top")

        if i == 1:
            article = articles_field.find('article', class_="item-news full-thumb article-topstory")
            article_url = article.find('p', class_="description").a['href']
            article_list.append(article_url)

        articles = articles_field.find(
            'div',
            class_="width_common list-news-subfolder list-news-folder-photo has-border-right").find_all('article')
        for article in articles:
            article_url = article.find('h2', class_="title-news").a['href']
            article_list.append(article_url)

    with open(DATA_DIR.joinpath('article_list.json'), 'w', encoding='utf-8') as fp:
        json.dump({'article_list': article_list}, fp, indent=4, ensure_ascii=False)


def build_data():
    with open(DATA_DIR.joinpath('article_list.json'), 'r', encoding='utf-8') as fp:
        article_list = json.load(fp)['article_list']

    image_caption_list = []
    http = urllib3.PoolManager()
    for article in tqdm(article_list):
        time.sleep(1)  # Slow down so server might think this is a human
        response = http.request('GET', article)
        soup = BeautifulSoup(response.data, 'lxml')
        if soup.find('div', class_="wrap_video clearfix"):
            continue
        else:
            try:
                caption = soup.find('div', class_="width-detail-photo").find('p', class_="description").contents[0]
                image_url = soup.find('picture').img['data-src']
                ic = ImageCaption(image_url, caption, article)
                image_caption_list.append(ic.to_dict())
            except AttributeError:
                continue

    with open(DATA_DIR.joinpath('image_caption_list.json'), 'w', encoding='utf-8') as fp:
        json.dump({'image_caption_list': image_caption_list}, fp, indent=4, ensure_ascii=False)


def clean_data():
    with open(DATA_DIR.joinpath('image_caption_list.json'), 'r', encoding='utf-8') as fp:
        image_caption_list = json.load(fp)['image_caption_list']

    http = urllib3.PoolManager()
    for image_caption in image_caption_list:
        if "</span>" in image_caption['caption']:
            response = http.request('GET', image_caption['article_url'])
            soup = BeautifulSoup(response.data, 'lxml')
            caption = soup.find('div', class_="width-detail-photo").find('p', class_="description").contents[1]
            image_caption['caption'] = caption

    with open(DATA_DIR.joinpath('image_caption_list.json'), 'w', encoding='utf-8') as fp:
        json.dump({'image_caption_list': image_caption_list}, fp, indent=4, ensure_ascii=False)


make_article_list()
build_data()
clean_data()
