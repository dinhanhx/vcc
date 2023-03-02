import codecs
import time
import random
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

VNANET_URL = r"https://vietnam.vnanet.vn/vietnamese/phong-su-anh"
HTML_DIR = Path(r"data/vnanet/vietnamese/phong-su-anh")
HTML_DIR.mkdir(parents=True, exist_ok=True)
START_INDEX = 2
END_INDEX = 40

driver = webdriver.Chrome()
driver.get(VNANET_URL)

# Get first page
with codecs.open(str(HTML_DIR.joinpath('1.html')), 'w', encoding='utf-8') as fp:
    time.sleep(random.randint(3, 5))
    fp.write(driver.page_source)

next_page_a_attribute = (
    lambda v: f"//a[@onclick='itemclick(this);' and @data-index='{v}']"
)  # noqa: E731
driver.find_element("xpath", next_page_a_attribute(START_INDEX)).click()

# Get pages in the middle
for i in range(START_INDEX, END_INDEX):
    WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element("xpath", next_page_a_attribute(i + 1))
    )

    with codecs.open(str(HTML_DIR.joinpath(f'{i}.html')), 'w', encoding='utf-8') as fp:
        time.sleep(random.randint(3, 5))
        fp.write(driver.page_source)

    driver.find_element("xpath", next_page_a_attribute(i + 1)).click()

# Get last page
with codecs.open(
    str(HTML_DIR.joinpath(f'{END_INDEX}.html')), 'w', encoding='utf-8'
) as fp:
    time.sleep(random.randint(3, 5))
    fp.write(driver.page_source)
