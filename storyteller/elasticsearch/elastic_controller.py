from elasticsearch import Elasticsearch


class ElasticController:
    def __init__(self,
                 cloud_id: str,
                 user_id: str,
                 user_pw: str,
                 index_name: str):
        self.elastic = Elasticsearch(cloud_id, http_auth=(user_id, user_pw))
        self.index = index_name

    def read(self,
             query: dict,
             highlight: dict = None):
        """
        :param query:
        :param highlight:
        '''
        >>> # Example input parameter
        >>> query = {
        >>>     'match_phrase': {
        >>>         'eg': {
        >>>             'query': query,
        >>>             'analyzer': 'nori'
        >>>         }
        >>>     }
        >>> }
        >>> highlight = {
        >>>     'fields': {
        >>>         'eg': {
        >>>             'type': 'plain',
        >>>             'fragment_size': 15,
        >>>             'number_of_fragments': 2,
        >>>             'fragmenter': 'span'
        >>>         }
        >>>     }
        >>> }
        '''
        :return:
        """
        return self.elastic.search(index=self.index, query=query, highlight=highlight)

    def write(self,
              info,
              bulk: bool):
        """
        :param bulk:
        :param info:
        :return:
        """

        if bulk:
            # TODO: Bulk upload 구현.
            return self.elastic.bulk(index=self.index, doc_type='_doc', body=info)
        else:
            return self.elastic.index(index=self.index, doc_type='_doc', document=info)

