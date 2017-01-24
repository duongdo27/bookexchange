from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from .models import Book, Section, BookSection, UserBook
from .form import UserBookForm
from django.shortcuts import redirect
import ipdb


class HomeView(TemplateView):
    template_name = 'index.html'


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"


class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        section_data = [x.section.__repr__()
                        for x in BookSection.objects.filter(book=self.object)]
        context['section_data'] = section_data
        user_book = UserBook.objects.filter(user=self.request.user, book=self.object).first()
        if user_book is None:
            user_book = UserBook.objects.create(user=self.request.user, book=self.object)
        form = UserBookForm(user_book.__dict__)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(BookDetailView, self).get_context_data(**kwargs)

        form = UserBookForm(request.POST)
        if form.is_valid():
            user_book = UserBook.objects.filter(user=self.request.user, book=self.object).first()

            if user_book:
                user_book.unit_price = form.data["unit_price"]
                user_book.quantity = form.data["quantity"]
                user_book.save()
        context['form'] = form
        return self.render_to_response(context)




