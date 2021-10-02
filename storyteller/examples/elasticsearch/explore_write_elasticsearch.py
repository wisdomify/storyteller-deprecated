from elasticsearch import Elasticsearch
from storyteller.paths import DATA_DIR
from storyteller.secrets import ELASTICSEARCH_PASSWORD
from os import path
import csv

def insertData(es : Elasticsearch,
               wisdom : str,
               eg : str):
    
    index="product_list"
    
    doc = {
        "wisdom" : wisdom,
        "eg" : eg
    }
    
    es.index(index="wisdom2eg", doc_type="_doc", body=doc)

cloud_id = "https://storyteller.es.asia-northeast3.gcp.elastic-cloud.com:9243/"
wisdom2eg_path= path.join(DATA_DIR, 'version_0/raw/wisdom2eg.tsv')
es = Elasticsearch(cloud_id, 
                   http_auth=("teang1995", ELASTICSEARCH_PASSWORD))

# print(es) 
#<Elasticsearch([{'host': 'storyteller.es.asia-northeast3.gcp.elastic-cloud.com', \
# 'port': 9243, 'use_ssl': True}])>

with open(wisdom2eg_path, 'r') as fh:
    f = csv.reader(fh, delimiter='\t')
    next(f, None)
    for row in f:
        # print(row)
        [wisdom, eg] = row
        insertData(es, wisdom, eg)
