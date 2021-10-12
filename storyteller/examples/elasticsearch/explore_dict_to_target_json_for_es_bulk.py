import json


def explore_dict_to_target_json_for_es_bulk():
    data = [
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 0},
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 1},
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 2},
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 3},
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 4},
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 5},
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 6},
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 7},
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 8},
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 9},
        {"source": 4, "title": "868", "sent": "test_sent", "sent_id": 10},
        {"source": 5, "title": "32963", "sent": "test_sent", "sent_id": 0},
        {"source": 5, "title": "32963", "sent": "test_sent", "sent_id": 1},
        {"source": 5, "title": "32963", "sent": "test_sent", "sent_id": 2},
        {"source": 5, "title": "32963", "sent": "test_sent", "sent_id": 3},
        {"source": 5, "title": "32963", "sent": "test_sent", "sent_id": 4},
        {"source": 2, "title": "43580", "sent": "test_sent", "sent_id": 0},
        {"source": 2, "title": "43580", "sent": "test_sent", "sent_id": 1},
        {"source": 2, "title": "43580", "sent": "test_sent", "sent_id": 2}
    ]

    cur_docs = '\n'.join(
        list(
            map(
                lambda doc: '{"index": {}}\n' + json.dumps(doc),
                data
            )
        )
    )

    print(cur_docs)


if __name__ == '__main__':
    explore_dict_to_target_json_for_es_bulk()
