
from typing import NoReturn
import requests
import typesense

from plugins.base import AbstractSearchBackend


class TypesenseBackend(AbstractSearchBackend):

    def __init__(self, schema=None, config=None):
        self.client = typesense.Client(config)
        self.schema = schema
        self.config = config

    @property
    def collection(self):
        return self.client.collections[self.collection_name]

    @property
    def documents(self):
        return self.collection.documents

    def create(self, document_data: dict):
        self.collection.documents.create(document_data)

    def update(self, document_data: dict):
        self.collection.documents.update(document_data)

    def create_or_update(self, document_data: dict):
        self.collection.documents.upsert(document_data)

    def delete(self, document_id: str):
        self.documents[document_id].delete()

    def search(self, query: str, fields: list, page: int = 1, document_per_page: int = 10) -> dict:
        search_parameters = {
            'q': query,
            'query_by': ','.join(fields),
            'per_page': document_per_page,
            'page': page
        }
        raw_response = self.documents.search(search_parameters)
        return self._parse(raw_response)

    def _parse(self, search_results: dict):
        results = []
        for hit in search_results.get('hits', []):
            document = hit.get('document', {})
            parsed_document = {field['name']: document.get(
                field['name']) for field in self.schema['fields']}
            results.append(parsed_document)
            response = {
                'count': search_results.get('found', 0),
                'page': search_results.get('page', 0),
                'results': results
            }
            return response

    def health(self, raise_on_unhealthy=False) -> dict | NoReturn:
        health_status = {}
        
        for node in self.config['nodes']:
            url = f"{node['protocol']}://{node['host']}:{node['port']}/health"
            try:
                response = requests.get(
                    url, timeout=self.config['connection_timeout_seconds'])
                if response.status_code == 200 and response.json().get('ok'):
                    health_status[node['host']] = 'healthy'
                else:
                    health_status[node['host']] = 'unhealthy'
                    if raise_on_unhealthy:
                        raise ConnectionError(
                            f'Typesense node {node} is not healthy')
            except requests.RequestException as e:
                health_status[node['host']] = f'unhealthy: {e}'
                if raise_on_unhealthy:
                    raise ConnectionError(
                        f'Typesense node {node} is not healthy')
                return health_status
