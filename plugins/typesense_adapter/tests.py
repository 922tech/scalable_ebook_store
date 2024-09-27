import unittest
from unittest.mock import MagicMock
from .typesense import TypesenseBackend


class TestTypesenceBackend(unittest.TestCase):

    def setUp(self):
        # Sample schema for the collection
        self.schema = {
            'name': 'books',
            'fields': [
                {'name': 'title', 'type': 'string'},
                {'name': 'author', 'type': 'string'}
            ]
        }

        # Initialize TypesenseBackend with the sample schema
        self.backend = TypesenseBackend(schema=self.schema)

        # Mock the client attribute directly on the backend
        self.backend.client = MagicMock()

    def test_create_document(self):
        # Mock the documents.create method
        mock_documents = self.backend.client.collections[self.schema['name']].documents
        mock_documents.create = MagicMock()

        # Data to insert
        document_data = {'title': '1984', 'author': 'George Orwell'}

        # Call the create method
        self.backend.create(document_data)

        # Assert that create was called with the correct data
        mock_documents.create.assert_called_once_with(document_data)

    def test_search_documents(self):
        # Mock the documents.search method and return a mock result
        mock_documents = self.backend.client.collections[self.schema['name']].documents
        mock_search_results = {
            'hits': [{'document': {'title': '1984', 'author': 'George Orwell'}}],
            'found': 1,
            'page': 1
        }
        mock_documents.search = MagicMock(return_value=mock_search_results)

        # Perform search
        query = '1984'
        fields = ['title', 'author']
        response = self.backend.search(query=query, fields=fields)

        # Assert that search was called with the correct parameters
        mock_documents.search.assert_called_once_with({
            'q': query,
            'query_by': ','.join(fields),
            'per_page': 10,
            'page': 1
        })

        # Assert the correct response is returned
        expected_response = {
            'count': 1,
            'page': 1,
            'results': [{'title': '1984', 'author': 'George Orwell'}]
        }
        self.assertEqual(response, expected_response)

    def test_delete_document(self):
        # Mock the documents['123'].delete method
        mock_documents = self.backend.client.collections[self.schema['name']].documents
        mock_document = mock_documents['123']
        mock_document.delete = MagicMock()

        # Call delete
        self.backend.delete(document_id='123')

        # Assert that delete was called with the correct document ID
        mock_document.delete.assert_called_once()


if __name__ == '__main__':
    unittest.main()
