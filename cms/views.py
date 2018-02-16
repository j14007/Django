from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views import generic

from cms.models import Book, Impression
from cms.forms import BookForm, ImpressionForm


class book_listView(generic.ListView):
    """書籍の一覧"""
    # return HttpResponse('書籍の一覧')
    # books = Book.objects.all().order_by('id')
    # return render(request, 'cms/book_list.html', {'books': books})
    model = Book
    template_name = 'cms/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        """Return the last five published questions."""
        return Book.objects.all().order_by('id')


def book_edit(request, book_id=None):
    """書籍の編集"""
    # return HttpResponse('書籍の編集')
    if book_id:  # book_idが指定されている
        book = get_object_or_404(Book, pk=book_id)
    else:  # book_idが指定されていない
        book = Book()

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('cms:book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'cms/book_edit.html', dict(form=form, book_id=book_id))


def book_del(request, book_id):
    """書籍の削除"""
    # return HttpResponse('書籍の削除')
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('cms:book_list')


class ImpressionList(generic.ListView):
    """感想の一覧"""
    context_object_name = 'impressions'
    template_name = 'cms/impression_list.html'
    paginate_by = 2  # 1ページは最大2件ずつでページングする

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['book_id'])
        impressions = book.impressions.all().order_by('id')
        self.object_list = impressions

        context = self.get_context_data(object_list=self.object_list, book=book)
        return self.render_to_response(context)


def impression_edit(request, book_id, impression_id=None):
    """感想の編集"""
    book = get_object_or_404(Book, pk=book_id)  # 親の書籍を読む
    if impression_id:  # impression_id が指定されている (修正時)
        impression = get_object_or_404(Impression, pk=impression_id)
    else:  # impression_id が指定されていない (追加時)
        impression = Impression()

    if request.method == 'POST':
        form = ImpressionForm(request.POST, instance=impression)  # POST された request データからフォームを作成
        if form.is_valid():  # フォームのバリデーション
            impression = form.save(commit=False)
            impression.book = book  # この感想の、親の書籍をセット
            impression.save()
            return redirect('cms:impression_list', book_id=book_id)
    else:  # GET の時
        form = ImpressionForm(instance=impression)  # impression インスタンスからフォームを作成

    return render(request,
                  'cms/impression_edit.html',
                  dict(form=form, book_id=book_id, impression_id=impression_id))


def impression_del(request, book_id, impression_id):
    """感想の削除"""
    impression = get_object_or_404(Impression, pk=impression_id)
    impression.delete()
    return redirect('cms:impression_list', book_id=book_id)