from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from storyteller.collect.utils.DBConnector import controller
from storyteller.collect.utils.proverbUtils import get_proverbs
from storyteller.paths import DATA_DIR


def get_examples_of(word: str):
    link = 'https://ko.dict.naver.com/#/search?range=example&query={query}'.format(query=word)

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    driver.implicitly_wait(2)

    egs = list()

    count = 1
    while True:
        driver.get(link + '&page={page}'.format(page=count))

        # Search result Null
        try:
            example_area = driver.find_element_by_class_name('has-saving-function')

        except:
            print('NO RESULT', end='')
            break

        if not example_area.text:
            break

        # example result area
        examples = example_area.find_elements_by_class_name('row')

        for example in examples:
            eg_text = example.find_element_by_class_name('origin').text.split(' → ')[0]
            egs.append(eg_text)

        print('.', end='')
        count += 1

    driver.quit()
    eg_df = pd.DataFrame(egs, columns=['example'])
    eg_df['wisdom'] = word
    eg_df = eg_df[['wisdom', 'example']]

    eg_df['date'] = datetime.today().date()
    eg_df['origin'] = 'naverDict'
    eg_df['eg_id'] = None
    eg_df['example_morph'] = None
    eg_df['prev'] = None
    eg_df['next'] = None
    eg_df['full'] = None

    return eg_df


def get_naverdict_examples_from(target_dictionary: str):
    wisdoms = get_proverbs(target_csv=target_dictionary + '.csv')

    base_df = pd.DataFrame()
    for idx, wisdom in enumerate(wisdoms):
        print('current({}/{}):'.format(idx + 1, len(wisdoms)), wisdom, '=>', end='')
        examples_df = get_examples_of(wisdom)
        if len(examples_df) > 0:
            base_df = base_df.append(examples_df)
        print()
    base_df.to_csv(DATA_DIR + '/examples/{}_naver.csv'.format(target_dictionary))


def save_naverdict_examples(of: str):
    wisdoms = controller.get_df_from_sql(target_query=f"select distinct wisdom from definition where origin='{of}'")['wisdom'].tolist()

    for idx, wisdom in enumerate(wisdoms):
        print('current({}/{}):'.format(idx + 1, len(wisdoms)), wisdom, '=>', end='')
        examples_df = get_examples_of(wisdom)
        if len(examples_df) > 0:
            examples_df['wisdom_from'] = of
            controller.save_df_to_sql(origin_df=examples_df, target_table_name='example',
                                      if_exists='append', index=False)
        print()


if __name__ == '__main__':
    save_naverdict_examples(of='namuwiki')
