# Vietnamese Conceptual Caption

- VCC: Vietnamese Conceptual Caption
- VCC++: VCC but with long description aka photo stories

# Citation 

Check out [CITATION](CITATION.cff) file

# Setup

```
pip install -e .
```

## Setup Selenium

```
python vcc/setup_webdriver.py
```

# Craw data
In other words, you build data from actual websites

## VNANET
[VCC]

[Source](https://vietnam.vnanet.vn/vietnamese/phong-su-anh)

```
python vcc/vnanet_download_html.py
python vcc/vnanet_build_data.py make-article-list
python vcc/vnanet_build_data.py build-data
```

8431 images with captions from 633 articles from 29/12/2022 to 26/01/2005

## VNEXPRESS

### Inforgraphics
[VCC]

[Source](https://vnexpress.net/infographics)

```
python vcc/vnexpress_inforgraphics_build_data.py make-article-list
python vcc/vnexpress_inforgraphics_build_data.py build-data
python vcc/vnexpress_inforgraphics_build_data.py clean-data
```

331 images with captions from 499 articles from 21/1/2023 14/12/2021 (there are articles with sole videos so the number of images is less than the number of articles)

### Anh
[VCC++]

[Source](https://vnexpress.net/anh)

```
python vcc/vnexpress_anh_build_data.py make-photo-story-list
python vcc/vnexpress_anh_build_data.py build-data
```

551 photo stories from 555 articles from 31/1/2023 to 18/11/2022 (videos and animated pictures such as gif or apng are not crawled) (there are 4 articles that don't follow the usual template)

## Dantri

[VCC] [VCC++]

[Source](https://dantri.com.vn/du-lich/video-anh/trang-1.htm)

```
python vcc/dantri_build_data.py make-article-list
python vcc/dantri_build_data.py build-data
```

64 (photo_story) + 53 (dmagazine) photo stories and 1431 images with captions from 600 articles from 25/01/2023 to 17/01/2020

⚠ NOTE:
- there are gifs, apng
- there are images WITHOUT captions
- sometimes in a certain article, the author uses 2 images with 1 caption/description hence **we** only take the **first one** in that pair.
