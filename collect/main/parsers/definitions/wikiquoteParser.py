from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from functools import reduce

from collect.main import paths


def get_html_from(link: str, target: str) -> pd.DataFrame:
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    driver.implicitly_wait(10)

    all_results = list(map(
        lambda char: (
            list(map(
                lambda wisdom, meaning: (wisdom.text, meaning.text),
                char.find_elements_by_tag_name('dt'), char.find_elements_by_tag_name('dd')
            ))
        ),
        driver.find_elements_by_tag_name(target)
    ))

    all_results = list(reduce(lambda prev, cur: prev + cur, all_results))

    driver.quit()

    return pd.DataFrame(all_results, columns=['wisdom', 'def_1'])


def get_wikiquote_definitions():
    get_html_from('https://ko.wikiquote.org/wiki/한국_속담', 'dl').to_csv(
        paths.DATA_DIR + '/definitions/wikiquote.csv')
