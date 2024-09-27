from apps.store.models import Payment, PaymentStatus


class StoreService:
    def __init__(self, book):
        self.book = book

    def can_download(self, user):
        if self.book.price == 0:
            return True
        return Payment.objects.filter(book_id=self.book.id, profile_id=user.id,
                                      status=PaymentStatus.SUCCESSFUL).exists()

    def validate_purchase(self, book_data, user):
        if not self.can_download(user):
            book_data.pop('file_url')
        return book_data
