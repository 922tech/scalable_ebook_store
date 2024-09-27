import sys
from django.conf import settings
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string

from plugins.base import AbstractSearchBackend, SingletonMetaClass


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


class StorageService(LazyObject, metaclass=SingletonMetaClass):

    def __init__(self, *args, **kwargs) -> None:
        self._wrapped = import_string(
            settings.CLOUD_SfileTORAGE_CLIENT_CONFIG['backend'])(
            *args, config=settings.CLOUD_STORAGE_CLIENT_CONFIG,
            **kwargs
        )
