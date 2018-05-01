from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [  
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]

# Add URLConf to create, update, and delete books
urlpatterns += [  
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/add_instance/', views.BookAddInstance.as_view(), name='add_instance'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]

# Purchase
urlpatterns += [
    path('book/<int:pk>/purchase/', views.BookPurchase.as_view(), name='book_purchase'),
]

#cart

urlpatterns += [
    path('cart/', views.CartView, name='cart'),
]

# books on loan to user
urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
	path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
]

urlpatterns += [   
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('book/<uuid:book_id>/borrow', views.borrow_book, name='borrow-book'),
    path('book/<uuid:book_id>/add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('book/<uuid:book_id>/remove-from-cart', views.remove_from_cart, name='remove-from-cart'),
]

urlpatterns += [
    path('signup/', views.signup, name='signup'),
]

urlpatterns += [
    path('checkout/<int:pk>/', views.ProfileCheckout.as_view(), name='checkout'),
]

urlpatterns += [
    path('success/', views.success_page, name='success'),
]
