from django.forms import ModelForm
from cms.models import Book, Impression


class BookForm(ModelForm):
    """書籍フォーム"""

    class Meta:
        model = Book
        fields = ('name', 'publisher', 'page')


class ImpressionForm(ModelForm):
    """感想のフォーム"""

    class Meta:
        model = Impression
        fields = ('comment',)
