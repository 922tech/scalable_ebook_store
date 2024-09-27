from django import forms

from apps.store.models import Book


class RegisterBookForm(forms.Form):
    file = forms.FileField()

    class Meta:
        model = Book
        exclude = ['id', 'created_at', 'updated_at']
