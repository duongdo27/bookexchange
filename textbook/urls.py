from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'book_detail/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book_detail'),
]