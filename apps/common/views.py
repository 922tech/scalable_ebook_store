from abc import abstractmethod
from rest_framework.viewsets import GenericViewSet


class BaseViewSet(GenericViewSet):
    pass


class SearchMixin:
    search_documents = None

    def search(self):
        pass
