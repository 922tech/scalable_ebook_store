import uuid
from django.contrib.postgres.indexes import HashIndex
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from apps.common.models import BaseModel

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.types import Validated
from plugins.registry import SearchBackend


class OrderStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    SHIPPED = 'shipped', _('Shipped')
    DELIVERED = 'delivered', _('Delivered')
    CANCELED = 'canceled', _('Canceled')


class PaymentGatewayChoices(models.TextChoices):
    STRIPE = 'stripe', _('Stripe')
    SADAD = 'sadad', _('Sadad')


class PaymentLogType(models.IntegerChoices):
    request = 0, _('Request')
    verify = 1, _('Verify')


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    SUCCESSFUL = 'successful', _('Successful')
    FAILED = 'failed', _('Failed')


class UploadStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    SUCCESSFUL = 'successful', _('Successful')
    FAILED = 'failed', _('Failed')


class FileUrlSchemaValidator:
    SCHEMA = {'status': str, 'url': str, 'is_public': bool}

    @staticmethod
    def validate_url(file_dict):
        URLValidator()(file_dict.get('url'))
        return file_dict

    @classmethod
    def schema_validator(cls, file_dict):
        if not set(file_dict) == set(cls.SCHEMA):
            raise ValidationError(
                f"Unexpected keys found in the value\
                 of file_field validation error: {set(file_dict) ^ set(cls.SCHEMA)}"
            )

        for field, field_type in cls.SCHEMA.items():
            if not isinstance(file_dict[field], field_type):
                raise ValidationError("Type mismatch for field '{}'".format(field))
        return file_dict


class Book(BaseModel):
    _file_dict_validators = [FileUrlSchemaValidator.schema_validator, FileUrlSchemaValidator.validate_url]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    author = models.CharField(max_length=255)
    pages = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    summary = models.TextField()
    file_dict = models.JSONField(validators=_file_dict_validators, default=dict)
    sample_file_dict = models.JSONField(validators=_file_dict_validators, default=dict)
    price = models.PositiveBigIntegerField()

    SEARCH_SCHEMA = {
        'name': 'books',
        'fields': [
            {'name': 'id', 'type': 'int64'},
            {'name': 'title', 'type': 'string'},
            {'name': 'author', 'type': 'string'},
            {'name': 'publication_date', 'type': 'string', 'facet': False},
            {'name': 'pages', 'type': 'int32', 'facet': False},
            {'name': 'cover_image', 'type': 'string', 'facet': False},
            {'name': 'summary', 'type': 'string'},
            {'name': 'file_url', 'type': 'string', 'facet': False},
            {'name': 'sample_file_url', 'type': 'string', 'facet': False}
        ]
    }

    documents = SearchBackend(schema=SEARCH_SCHEMA)

    def __str__(self):
        return self.title

    def to_document(self):
        self.clean_fields()
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'publication_date': self.publication_date.isoformat() if self.publication_date else "",
            'pages': self.pages if self.pages else 0,
            'cover_image': self.cover_image.url if self.cover_image else "",
            'summary': self.summary if self.summary else "",
            'file_dict': self.file_dict.get('url', ''),
            'sample_file_dict': self.sample_file_dict.get('url', ''),
        }


class Review(BaseModel):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='reviews'
    )
    user = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()


class PaymentDataValidator:
    """
    This class wraps the schema validation of data returned by payment the gateways and setting tracking code
    """

    @staticmethod
    def stripe_verify(instance) -> Validated[dict]:
        # set tracking code and checking schema
        return instance

    @staticmethod
    def paypal_verify(instance) -> Validated[dict]:
        # set tracking code and checking schema
        return instance

    @staticmethod
    def sadad_verify(instance) -> Validated[dict]:
        # set tracking code and checking schema
        return instance

    @staticmethod
    def stripe_request(instance) -> Validated[dict]:
        # set tracking code and checking schema
        return instance

    @staticmethod
    def paypal_request(instance) -> Validated[dict]:
        # set tracking code and checking schema
        return instance

    @staticmethod
    def sadad_request(instance) -> Validated[dict]:
        # set tracking code and checking schema
        return instance


class PaymentDataLog(BaseModel):
    metadata = models.JSONField(default=dict, help_text="Payment metadata")
    gateway = models.CharField(max_length=63, choices=PaymentGatewayChoices.choices)
    tracking_code = models.CharField(max_length=255, help_text="a value from metadata that is used as tracking code")
    log_type = models.IntegerField(choices=PaymentLogType.choices)

    def clean(self) -> Validated[None]:
        """Checks if metadata of payment is correct according to the gateway"""
        getattr(PaymentDataValidator, self.gateway)(self)
        super().clean()

    class Meta:
        indexes = [
            HashIndex(fields=['tracking_code'], name='tracking_code_idx'),
        ]


class Payment(BaseModel):
    payment_id = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='payments', db_index=True, editable=False)
    amount = models.PositiveBigIntegerField(editable=False)
    status = models.CharField(max_length=12, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    log = models.OneToOneField(PaymentDataLog, on_delete=models.DO_NOTHING, editable=False, blank=True, null=True)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            HashIndex(fields=['payment_id'], name='payment_id_idx'),
        ]
