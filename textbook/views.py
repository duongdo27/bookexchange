from django.views.generic import TemplateView, DetailView
from .models import Book, Section, BookSection

class HomeView(TemplateView):
    template_name = 'index.html'


class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"

