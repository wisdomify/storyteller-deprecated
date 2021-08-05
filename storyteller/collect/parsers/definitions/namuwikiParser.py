from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from storyteller.collect.utils.DBConnector import controller


def get_html_from(link: str, target: str) -> pd.DataFrame:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # namu wiki crawling fails when browser is opened with headless parameter.

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    driver.implicitly_wait(10)

    all_results = list(map(
        lambda char: (char.text.split(':')[0], ':'.join(char.text.split(':')[1:])),
        driver.find_elements_by_class_name(target)[3:]
    ))

    driver.quit()

    return pd.DataFrame(all_results, columns=['wisdom', 'definition'])


def save_namuwiki_definitions():
    df = get_html_from('https://namu.wiki/w/속담/한국', 'wiki-paragraph')
    df['origin'] = 'namuwiki'
    df['date'] = datetime.today().date()

    controller.save_df_to_sql(origin_df=df,
                              target_table_name='definition', if_exists='append', index=False)


if __name__ == '__main__':
    save_namuwiki_definitions()
