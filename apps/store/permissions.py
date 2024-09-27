from apps.common.permissions import BasePermission
from apps.store.models import Book
from apps.store.services import StoreService


class DownloadBookPermission(BasePermission):
    def has_object_permission(self, request, view, obj: Book):
        return StoreService(book=obj).can_download(request.user)
