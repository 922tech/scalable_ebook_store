import sys
from typing import NoReturn
from django.conf import settings
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string
from abc import ABC, abstractmethod


class SingletonMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
            return cls._instances[cls]


class AbstractSearchBackend(ABC):
    @abstractmethod
    def create(self, document_data: dict):
        """Create or update a document in the search index"""
        pass

    @abstractmethod
    def update(self, document_data: dict):
        """Create or update a document in the search index"""
        pass

    @abstractmethod
    def delete(self, document_id: str):
        """Delete a document from the search index"""
        pass

    @abstractmethod
    def search(self, query: str, fields: list):
        """Search for documents in the search index"""
        pass

    @abstractmethod
    def create_or_update(self, document_data: dict):
        pass

    @abstractmethod
    def health(self) -> None | NoReturn:
        pass


class SearchBackend(LazyObject):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._wrapped = import_string(settings.DATABASES['search']['backend'])(
            *args, config=settings.DATABASES['search']['config'], **kwargs)

        if not isinstance(self._wrapped, AbstractSearchBackend):
            raise TypeError(
                f'Search backend {self._wrapped} does not implement AbstractSearchBackend')
        if {'migrate', 'makemigrations'} & set(sys.argv):
            self._wrapped.health()


class AbstractStorageServiceAdapter(ABC):
    @abstractmethod
    def get(self, file_name, is_public=False) -> str:
        """
        Retrieve the file from storage, either publicly accessible or presigned.
        """
        pass

    @abstractmethod
    def save(self, file, deep_check=False, is_public=False) -> dict:
        """
        Save the file to the storage. Optionally check for duplicates and store publicly or privately.
        """
        pass

    @abstractmethod
    def delete(self, file_name) -> dict:
        """
        Delete the file from storage.
        """
        pass

    @abstractmethod
    def get_temp_upload_url(self, file_name) -> dict:
        """
        Delete the file from storage.
        """
        pass
