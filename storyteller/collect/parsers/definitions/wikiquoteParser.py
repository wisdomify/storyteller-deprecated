from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from functools import reduce

from storyteller import paths


def get_html_from(link: str, target: str) -> pd.DataFrame:
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    driver.implicitly_wait(10)

    all_results = list(map(
        lambda char: (
            list(map(
                lambda row: (row.text.split(':')[0], row.text.split(':')[-1] if len(row.text.split(':')) > 1 else None),
                char.find_elements_by_tag_name('li')[14:]
            ))
        ),
        driver.find_elements_by_class_name(target)
    ))

    all_results = list(reduce(lambda prev, cur: prev + cur, all_results))

    driver.quit()

    return pd.DataFrame(all_results, columns=['wisdom', 'def_1'])


def get_wikiquote_definitions():
    get_html_from('https://ko.wikiquote.org/wiki/가나다순_한국_속담', 'mw-parser-output').to_csv(
        paths.DATA_DIR + '/definitions/wikiquote.csv')
