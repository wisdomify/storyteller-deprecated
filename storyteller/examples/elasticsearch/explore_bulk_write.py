from storyteller.elasticsearch.elastic_controller import ElasticController


def explore_bulk():
    cloud_id = "https://storyteller.es.asia-northeast3.gcp.elastic-cloud.com:9243/"
    user_id = "teang1995"
    user_pw = "wisdom2eg"

    es = ElasticController(
        cloud_id=cloud_id,
        user_id=user_id,
        user_pw=user_pw,
        index_name='testiiing'
    )

    res = es.write(
        bulk=True,
        info='{"index": {"_index": "testiiing", "_id": "1"}}\n'
             '{"source": 4, "title": "3572", "sents": "sent1"}\n'
             '{"index": {"_index": "testiiing", "_id": "2"}}\n'
             '{"source": 2, "title": "45475", "sents": "sent2"}\n'
             '{"index": {"_index": "testiiing", "_id": "3"}}\n'
             '{"source": 9, "title": "96346", "sents": "sent3"}\n'
             '{"index": {"_index": "testiiing", "_id": "4"}}\n'
             '{"source": 8, "title": "30875", "sents": "sent4"}\n'
    )

    print(res)


if __name__ == '__main__':
    explore_bulk()
