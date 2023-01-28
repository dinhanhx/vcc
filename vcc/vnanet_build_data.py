import json
import random
import time
from pathlib import Path

import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm

from vcc.image_caption import ImageCaption

HTML_DIR = Path(r"data/vnanet/vietnamese/phong-su-anh")
DATA_DIR = Path(r"data/vnanet/vietnamese/")
START_INDEX = 1
END_INDEX = 40


def make_article_list():
    article_list = []
    for i in range(START_INDEX, END_INDEX+1):
        html_file = HTML_DIR.joinpath(f'{i}.html')
        soup = BeautifulSoup(open(html_file, 'r', encoding='utf-8'), 'lxml')

        for div in soup.find_all('div', class_="bavn-small-news"):
            article_url = div.find('a', class_="thumb-img thumb-img-16x9")['href']
            article_list.append(article_url)

    with open(DATA_DIR.joinpath('article_list.json'), 'w', encoding='utf-8') as fp:
        json.dump({'article_list': article_list}, fp, indent=4, ensure_ascii=False)


def build_data():
    with open(DATA_DIR.joinpath('article_list.json'), 'r', encoding='utf-8') as fp:
        article_list = json.load(fp)['article_list']

    image_caption_list = []
    http = urllib3.PoolManager()
    for article_url in tqdm(article_list):
        time.sleep(random.randint(1, 3))  # Slow down so server might think this is a human
        response = http.request('GET', article_url)
        soup = BeautifulSoup(response.data, 'lxml')

        for div in soup.find_all('div', class_="uk-flex uk-flex-column"):
            div_a = div.find('a', class_="uk-inline")
            ic = ImageCaption(
                image_url=div_a['href'],
                caption=div_a['data-caption'],
                article_url=article_url
            )
            image_caption_list.append(ic.to_dict())

    with open(DATA_DIR.joinpath('image_caption_list.json'), 'w', encoding='utf-8') as fp:
        json.dump({'image_caption_list': image_caption_list}, fp, indent=4, ensure_ascii=False)


make_article_list()
build_data()
