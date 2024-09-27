from rest_framework import serializers

from apps.common.serializers import BaseModelSerializer, WriteOnceMixin

from .models import Book, Review, Payment


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'uuid', 'title', 'publication_date', 'author', 'pages',
            'cover_image', 'summary', 'file_dict', 'sample_file_dict', 'price'
        ]
        read_only_fields = ['uuid']


class BookListSerializer(BaseModelSerializer):
    file_url = serializers.CharField(source='file_dict.url')
    sample_file_url = serializers.CharField(source='file_dict.url')

    class Meta:
        model = Book
        read_only_fields = [
            'title',
            'publication_date',
            'author',
            'pages',
            'cover_image',
            'summary',
            'price',
            'sample_file_url',
            'file_url'
        ]
        filed = read_only_fields


class ReviewSerializer(WriteOnceMixin, BaseModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        request = self.context['request']
        if request.method.lower() in {'get', 'post'}:
            return obj.user.username
        return request.user

    class Meta:
        model = Review
        write_only_fields = ['book', ]
        fields = ['user', 'rating', 'comment', ] + write_only_fields


class PaymentSerializer(WriteOnceMixin, BaseModelSerializer):
    amount = serializers.IntegerField(source='book.price', read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.filter())

    class Meta:
        model = Payment
        extra_kwargs = {
            'amount': {'read_only': True},
            'status': {'read_only': True},
        }
        write_once_fields = ['order', ]

        fields = [
            'order',
        ]
