import json
from pathlib import Path
from urllib.parse import urlparse
from typing import List, Union

import click
import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm

from vcc.image_text import ImageCaption, ImageDescription, PhotoStory
from vcc.ordered_commands import OrderedCommands

DATA_DIR = Path(r"data/dantri")
START_INDEX = 1
END_INDEX = 30


@click.group(cls=OrderedCommands)
def cli():
    """Welcome to dantri crawler, please run commands in the order that you see in this help text"""
    pass


@cli.command()
def make_article_list():
    article_list = []
    http = urllib3.PoolManager()
    for i in tqdm(range(START_INDEX, END_INDEX + 1)):
        dantri_page = f"https://dantri.com.vn/du-lich/video-anh/trang-{i}.htm"
        response = http.request('GET', dantri_page)
        soup = BeautifulSoup(response.data, 'lxml')

        h3_tag_list = soup.findAll('h3', class_="article-title")
        for h3_tag in h3_tag_list:
            article_page = urlparse(h3_tag.find('a')['href'])
            article_page = article_page._replace(scheme="https")
            article_page = article_page._replace(netloc="dantri.com.vn")
            article_list.append(
                f"{article_page.scheme}://{article_page.netloc}{article_page.path}"
            )

    with open(DATA_DIR.joinpath('article_list.json'), 'w', encoding='utf-8') as fp:
        json.dump({'article_list': article_list}, fp, indent=4, ensure_ascii=False)


def get_emagazine_category(soup: BeautifulSoup):
    try:
        div_top = soup.find('div', class_="top")
        div_emagazine_category = div_top.find('div', class_="emagazine-category")
        return (
            div_emagazine_category.find('a')['href']
            .replace('/', '')
            .replace('.htm', '')
        )
    except AttributeError:
        return None


def make_image_caption_list(soup: BeautifulSoup, article_url: str) -> List[dict]:
    image_caption_list: List[dict] = []
    for figure_tag in soup.find_all('figure', class_="image align-center"):
        url = figure_tag.find('img')['data-original']
        figcaption = figure_tag.find('figcaption')
        if figcaption:
            caption = figcaption.get_text()
        else:
            caption = ''
        image_caption_list.append(ImageCaption(url, caption, article_url).to_dict())

    return image_caption_list


def make_photo_story(soup: BeautifulSoup, article_url: str) -> Union[dict, None]:
    # handle Photo Story article
    if soup.find('h1', class_="e-magazine__title"):
        title = soup.find('h1', class_="e-magazine__title").get_text()
    else:
        # handle Dmagazine article
        title = soup.find('div', class_="e-magazine__cover").find('img')['alt']

    div_emagazine_body = soup.find('div', class_="e-magazine__body")

    contents: List[ImageDescription] = []
    cache_img_url: str = ""
    cache_description: List[str] = []

    for tag in div_emagazine_body:
        if tag.name == 'figure' and tag['class'][0] == 'image' and tag.contents:
            # The usual case
            contents.append(
                ImageDescription(str(cache_img_url), cache_description.copy())
            )
            cache_description = []
            cache_img_url = tag.find('img')['data-original']

        try:
            if tag.name == 'div' and tag['class'][0] == 'photo-grid':
                # The case that the author uses 2 images with 1 caption/description
                contents.append(
                    ImageDescription(str(cache_img_url), cache_description.copy())
                )
                cache_description = []
                cache_img_url = (
                    tag.find('div', class_="photo-row")
                    .find('figure', class_="image")
                    .find('img')['data-original']
                )
        except KeyError:
            pass

        if tag.name == 'p':
            cache_description.append(tag.get_text())

    contents.append(ImageDescription(str(cache_img_url), cache_description.copy()))
    contents.pop(0)
    return PhotoStory(contents, article_url, title).to_dict()


@cli.command()
def build_data():
    with open(DATA_DIR.joinpath('article_list.json'), 'r', encoding='utf-8') as fp:
        article_list = json.load(fp)['article_list']

    photo_story_dict = {
        'photo-story': {
            'list': [],
            'path': DATA_DIR.joinpath('photo_story', 'photo_story_list.json'),
        },
        'dmagazine': {
            'list': [],
            'path': DATA_DIR.joinpath('dmagazine', 'photo_story_list.json'),
        },
    }

    image_caption_list = []
    http = urllib3.PoolManager()
    for idx, url in enumerate(tqdm(article_list)):
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, 'lxml')
        category = get_emagazine_category(soup)
        if not category:
            image_caption_list += make_image_caption_list(soup, url)
        else:
            photo_story = make_photo_story(soup, url)
            if photo_story:
                photo_story_dict[category]['list'].append(photo_story)

    with open(
        DATA_DIR.joinpath('others', 'image_caption_list.json'), 'w', encoding='utf-8'
    ) as fp:
        json.dump(
            {'image_caption_list': image_caption_list}, fp, indent=4, ensure_ascii=False
        )

    for _, value in photo_story_dict.items():
        with open(value['path'], 'w', encoding='utf-8') as fp:
            json.dump(
                {'photo_story_list': value['list']}, fp, indent=4, ensure_ascii=False
            )


if __name__ == '__main__':
    cli()
