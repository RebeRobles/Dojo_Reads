from django.urls import path
from . import views


urlpatterns = [
    path('', views.book, name='book'),
    path('add', views.add, name='add'),
    path('add_book', views.create_book),
    path('logout', views.logout, name='logout'),
    path('delete/<review_id>', views.delete_review, name='delete_review'),
    path('<book_id>', views.book_id, name='book_id'),
    path('<book_id>/edit_review', views.edit_review, name='edit_review'),
    path('<user_id>', views.user_id, name='user_id'),  
]