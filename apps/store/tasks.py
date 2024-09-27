from celery import shared_task
from .models import Book


@shared_task
def sync_book_to_typesense(book_instance):
    # TODO: log start of task with parameters
    Book.documents.create_or_update(book_instance.to_document())
    # TODO: log task success with params


@shared_task
def remove_book_from_typesense(book_id: int):
    # TODO: log start of task with parameters
    Book.documents.delete(book_id)
    # TODO: log task success with params


@shared_task
def check_upload_status(book_id: int):
    # TODO: update book status if it was uploaded and make change in upload status of book
    pass
