from django.views.generic import TemplateView, DetailView, ListView
from .models import Book, Section, BookSection


class HomeView(TemplateView):
    template_name = 'index.html'


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"


class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"

