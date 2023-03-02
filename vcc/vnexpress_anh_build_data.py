import json
import random
import time
from pathlib import Path
from typing import List

import click
import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm

from vcc.image_text import ImageDescription, PhotoStory
from vcc.ordered_commands import OrderedCommands

DATA_DIR = Path(r"data/vnexpress/anh")
START_INDEX = 1
END_INDEX = 20


@click.group(cls=OrderedCommands)
def cli():
    """Welcome to vnexpress anh crawler, please run commands in the order that you see in this help text"""
    pass


@cli.command()
def make_photo_story_list():
    photo_story_url_list = []
    http = urllib3.PoolManager()
    for i in tqdm(range(START_INDEX, END_INDEX + 1)):
        time.sleep(
            random.randint(1, 3)
        )  # Slow down so server might think this is a human
        if i == 1:
            anh_page = "https://vnexpress.net/anh"
        else:
            anh_page = f"https://vnexpress.net/anh-p{i}"
        response = http.request('GET', anh_page)
        soup = BeautifulSoup(response.data, 'lxml')
        articles_field = soup.find('div', class_="col-left-top")

        if i == 1:
            article = articles_field.find(
                'article', class_="item-news full-thumb article-topstory"
            )
            article_url = article.find('p', class_="description").a['href']
            photo_story_url_list.append(article_url)

        articles = articles_field.find(
            'div',
            class_="width_common list-news-subfolder list-news-folder-photo has-border-right",
        ).find_all('article')
        for article in articles:
            article_url = article.find('h2', class_="title-news").a['href']
            photo_story_url_list.append(article_url)

    with open(
        DATA_DIR.joinpath('photo_story_url_list.json'), 'w', encoding='utf-8'
    ) as fp:
        json.dump(
            {'photo_story_url_list': photo_story_url_list},
            fp,
            indent=4,
            ensure_ascii=False,
        )


@cli.command()
def build_data():
    with open(
        DATA_DIR.joinpath('photo_story_url_list.json'), 'r', encoding='utf-8'
    ) as fp:
        photo_story_url_list = json.load(fp)['photo_story_url_list']

    photo_story_list = []
    skip_list = []
    http = urllib3.PoolManager()
    for url in tqdm(photo_story_url_list):
        try:
            response = http.request('GET', url)
            soup = BeautifulSoup(response.data, 'lxml')

            contents: List[ImageDescription] = []
            article_tag = soup.find('article', class_="fck_detail", id="lightgallery")
            for div_tag in article_tag.find_all(
                'div', class_='item_slide_show clearfix'
            ):
                description = []
                for p_tag in div_tag.find('div', class_='desc_cation').find_all('p'):
                    p_tag_content_list = []
                    for p_tag_content in p_tag:
                        if isinstance(p_tag_content, str):
                            p_tag_content_list.append(p_tag_content)
                        else:
                            p_tag_content_list.append(p_tag_content.get_text())
                    description.append(' '.join(p_tag_content_list))

                image_description = ImageDescription(
                    div_tag.find('div', class_='block_thumb_slide_show')['data-src'],
                    description=description,
                )
                contents.append(image_description)

            photo_story = PhotoStory(
                contents=contents,
                article_url=url,
                title=soup.find('h1', class_="title-detail").get_text(),
            )
            photo_story_list.append(photo_story.to_dict())
        except AttributeError:
            skip_list.append(url)

    with open(DATA_DIR.joinpath('photo_story_list.json'), 'w', encoding='utf-8') as fp:
        json.dump(
            {'photo_story_list': photo_story_list}, fp, indent=4, ensure_ascii=False
        )

    with open(DATA_DIR.joinpath('skip_list.json'), 'w', encoding='utf-8') as fp:
        json.dump({'skip_list': skip_list}, fp, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    cli()
