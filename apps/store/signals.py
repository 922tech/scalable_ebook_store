from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book
from .tasks import sync_book_to_typesense, remove_book_from_typesense


@receiver(post_save, sender=Book)
def sync_book(sender, instance, **kwargs):
    sync_book_to_typesense.delay(instance.to_document())


@receiver(post_delete, sender=Book)
def remove_book(sender, instance, **kwargs):
    remove_book_from_typesense.delay(instance.to_document())
