import os

import requests
import xmltodict as xmltodict
import pandas as pd

import secrets
from collect.main import paths


def get_opendict_definitions():

    BASE_URL = 'https://opendict.korean.go.kr/api/search'
    KEY = secrets.OPENDICT_API_KEY

    params = {
        'key': KEY,
        'sort': 'dict',
        'advanced': 'y',
        'method': 'wildcard',
        'type1': 'proverb',
        'type3': 'general',
        'target_type': 'search',
        'q': '.',
        'num': '20'
    }

    for start in range(1, 422):
        params['start'] = str(start)
        if os.path.isfile(paths.DATA_DIR+'/definitions/opendict/{start}_{end}.csv'
                                  .format(start=params['start'], end=int(params['start']) + int(params['num']) - 1)):
            print('EXIST: {}'.format(start + 1))
            continue

        res = requests.get(BASE_URL, params=params)
        res_tree = xmltodict.parse(res.text)

        while 'error' in res_tree.keys() or 'item' not in res_tree['channel'].keys():
            res = requests.get(BASE_URL, params=params)
            res_tree = xmltodict.parse(res.text)

        res_proverbs = list(map(
            lambda row: (row['sense']['target_code'], row['word'], row['sense']['definition']),
            res_tree['channel']['item']
        ))

        res_proverbs_pd = pd.DataFrame(res_proverbs, columns=['code', 'wisdom', 'def'])
        print("current start: {}\t current length: {}".format(start, len(res_proverbs_pd)))
        print(res_proverbs_pd.head(1))

        res_proverbs_pd.to_csv(paths.DATA_DIR+'/definitions/opendict/{start}.csv'.format(start=params['start']))
