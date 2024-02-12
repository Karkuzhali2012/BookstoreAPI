from django.urls import path
from books.views import (AuthorListView, AuthorDetailView, BookListView, BookDetailView, 
                        GetAuthorList, GetBookList)

urlpatterns = [
    path('authors/', AuthorListView.as_view()),
    path('authors/<int:id>/', AuthorDetailView.as_view()),
    path('books/', BookListView.as_view()),
    path('books/<int:id>/', BookDetailView.as_view()),
    path('listing-all-authors/', GetAuthorList.as_view()),
    path('listing-all-books/', GetBookList.as_view()),
]