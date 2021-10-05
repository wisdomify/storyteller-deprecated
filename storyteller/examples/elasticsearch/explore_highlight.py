from elasticsearch import Elasticsearch
from storyteller.paths import DATA_DIR
from storyteller.secrets import ELASTICSEARCH_PASSWORD
from os import path
import csv


# print(es) 
# <Elasticsearch([{'host': 'storyteller.es.asia-northeast3.gcp.elastic-cloud.com', \
# 'port': 9243, 'use_ssl': True}])>

def searchAPI(es: Elasticsearch,
              index: str,
              query: str):
    body = {
        'match_phrase': {
            'eg': {
                'query': query,
                'analyzer': 'nori'
            }
        }
    }
    highlight = {
        'fields': {
            'eg': {
                'type': 'plain',
                'fragment_size': 15,
                'number_of_fragments': 2,
                'fragmenter': 'span'
            }
        }
    }
    res = es.search(index=index, query=body, highlight=highlight)
    return res


def main():
    query = '산 넘어 산'
    cloud_id = "https://storyteller.es.asia-northeast3.gcp.elastic-cloud.com:9243/"
    es = Elasticsearch(cloud_id,
                       http_auth=("teang1995", ELASTICSEARCH_PASSWORD))

    res = searchAPI(es, 'wisdom_test', query)
    print(res)
    '''
    {'took': 3, 'timed_out': False, '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, \
    'hits': {'total': {'value': 1, 'relation': 'eq'}, 'max_score': 1.0, 'hits': [{'_index': 'wisdom2eg', '_type': '_doc', \
    '_id': '4-hBMHwBo8ESdJpAdGPQ', '_score': 1.0, '_source': {'wisdom': '산 넘어 산', 'eg': '텐트나 담요 등 구호물자를 노린 약탈이 잇따르고 있다.'}}]}}
    '''


if __name__ == "__main__":
    main()
