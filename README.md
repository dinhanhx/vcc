# Vietnamese Conceptual Caption

# Setup

```
pip install -e .
```

## Setup Selenium

```
python vcc/setup_webdriver.py
```

## VNANET

```
python vcc/vnanet_download_html.py
python vcc/vnanet_build_data.py make-article-list
python vcc/vnanet_build_data.py build-data
```

8431 images with captions from 633 articles from 26/01/2005 to 29/12/2022

## VNEXPRESS

### Inforgraphics

```
python vcc/vnexpress_inforgraphics_build_data.py make-article-list
python vcc/vnexpress_inforgraphics_build_data.py build-data
python vcc/vnexpress_inforgraphics_build_data.py clean-data
```

331 images with captions from 499 articles from 14/12/2021 to 21/1/2023 (there are articles with sole videos so the number of images is less than the number of articles)
