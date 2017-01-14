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

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        section_data = [x.section.__repr__()
                        for x in BookSection.objects.filter(book=self.object)]
        print section_data
        context['section_data'] = section_data
        return context

