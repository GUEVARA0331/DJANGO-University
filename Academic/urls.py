from django.urls import path
from . import views
from django.conf import settings 
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('formContact', views.formContact, name='formContact'),
    path('books', views.books, name='books'),
    path('book/add', views.addBook, name='addBook'),
    path('book/edit', views.editBook, name='editBook'),
    path('book/delete/<int:id>', views.deleteBook, name='deleteBook'),
    path('book/edit/<int:id>', views.editBook, name='editBook'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)