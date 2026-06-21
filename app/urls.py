from django.urls import path
from app.views import  (
    book_detail_view, book_list_view,book_create_view,
    book_delete_view, author_list, author_create,BookListAPIVew, BookDetailAPIVew, AuthorListAPIVew,
    AuthorDetailAPIVew
)
urlpatterns = [
    path('', book_list_view, name='book-list'),
    path('<int:pk>/', book_detail_view, name='book-detail'),
    path('<int:pk>/delete/', book_delete_view, name='book-delete'),
    path('<int:pk>/authors/', author_list, name='author-list'),
    path('<int:pk>/authors/create/', author_create, name='author-create'),
    path('book/new/', book_create_view, name='book-new'),
]

#API
urlpatterns = [
    path('api/books/', BookListAPIVew.as_view(), name='book-list-api'),
    path('api/books/<int:pk>/', BookDetailAPIVew.as_view(), name='book-detail'),
    path('api/authors/', AuthorListAPIVew.as_view(), name='author-list'),
    path('api/authors/, AuthorDetailAPIVew/', AuthorDetailAPIVew.as_view(), name='author-detail'),
]