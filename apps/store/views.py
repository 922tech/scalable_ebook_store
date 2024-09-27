from datetime import timedelta
from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework import permissions

from plugins.registry import StorageService
from .permissions import DownloadBookPermission
from .serializers import BookSerializer, PaymentSerializer, BookListSerializer
from apps.common.permissions import IsAdmin, ReadOnly
from apps.common.views import BaseViewSet, SearchMixin
from apps.store.models import Book, PaymentStatus
from .models import Payment
from rest_framework.decorators import action

from .services.store_services import StoreService
from apps.store.tasks import check_upload_status

storage_service = StorageService()


class BookViewSet(SearchMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, BaseViewSet):
    queryset = Book.objects.all()
    search_documents = Book.documents
    permission_classes = [IsAdmin | ReadOnly]

    def get_serializer_class(self):
        if self.action is 'list':
            return BookListSerializer
        return BookSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_data = self.get_serializer_class()(instance).data
        data = StoreService(instance).validate_purchase(instance_data, request.user)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request, *args, **kwargs):
        search_phrase = request.query_params.get('search_phrase', '')
        fields = request.query_params.getlist('fields', [])

        if not search_phrase or not fields:
            return Response(
                {"error": "search_phrase and fields are required parameters"},
                status=status.HTTP_400_BAD_REQUEST
            )
        search_results = self.search_documents.search(query=search_phrase, fields=fields)
        return Response(search_results)

    @action(detail=True, methods=['post', 'patch'], url_path='upload')
    def upload(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        is_public = bool(request.query_params.get('sample_file'))
        upload_link = storage_service.get_temp_upload_url(instance.uuid, expiry=timedelta(hours=1), is_public=is_public)
        # INVARIANT: client app must set the file name to book uuid
        check_upload_status.async_apply(countdown=settings.FILE_UPLOAD_CHECK_DELAY, args=[pk])
        return Response({'upload_link': upload_link}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='download', url_name='download',
            permission_classes=[DownloadBookPermission])
    def download_complete_book(self, request, *args, **kwargs):
        book = self.get_object()
        return StreamingHttpResponse(
            storage_service.get_object(book.uuid),
            content_type='application/octet-stream'
        )


class PaymentView(mixins.CreateModelMixin, mixins.UpdateModelMixin, BaseViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field = 'payment_id'

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        payment = self.get_object()
        payment.payment_status = PaymentStatus.SUCCESSFUL
        payment.save()
        return Response({"status": "successful"})
