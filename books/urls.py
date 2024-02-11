from django.urls import path
from books.views import AuthorListView, AuthorDetailView, BookListView, BookDetailView

urlpatterns = [
    path('authors/', AuthorListView.as_view()),
    path('authors/<int:id>/', AuthorDetailView.as_view()),
    path('books/', BookListView.as_view()),
    path('books/<int:id>/', BookDetailView.as_view()),
]