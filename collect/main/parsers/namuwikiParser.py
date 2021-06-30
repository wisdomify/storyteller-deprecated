import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from collect.main import paths


def get_html_from(link: str, target: str) -> pd.DataFrame:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # namu wiki crawling fails when browser is opened with headless parameter.

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    driver.implicitly_wait(10)

    all_results = list(map(
        lambda char: (char.text.split(':')[0], ':'.join(char.text.split(':')[1:])),
        driver.find_elements_by_class_name(target)
    ))

    driver.quit()

    return pd.DataFrame(all_results, columns=['wisdom', 'def_1'])


get_html_from('https://namu.wiki/w/속담/한국', 'wiki-paragraph').to_csv(paths.DATA_DIR+'/definitions/namuwiki.csv')
