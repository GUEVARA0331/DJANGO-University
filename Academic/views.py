from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPAuthenticationError
from socket import gaierror
from .models import Book, Career
from .forms import Book, BookForm
import os
from django.conf import settings 

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def contact(request): 
    if request.method == "POST": 
        subject = request.POST['subject']
        message = request.POST['message']+" / Email: "+request.POST['email']
        email_from = settings.EMAIL_HOST_USER
        email_to = [settings.EMAIL_HOST_USER]
        try:
            send_mail(subject, message, email_from, email_to, fail_silently=False)
            messages.success(request, 'Mensaje de contacto enviado')
        except SMTPAuthenticationError as e:
            messages.error(request, 'Autenticación del HOST_USER de SMTP gmail rechazada.')
        except gaierror as e:
            messages.warning(request, 'Verifica su conexión de internet e intenta nuevamente.')
        return redirect(to='formContact')

def formContact(request): 
    return render(request, 'pages/contact.html')

def books(request): 
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books':books})

def addBook(request): 
    form = BookForm(request.POST or None, request.FILES or None)
    if form.is_valid(): 
        form.save()
        messages.success(request, 'Libro registrado exitosamente.')
        return redirect('books')
    return render(request, 'books/add.html', {'form':form})

def deleteBook(request, id): 
    book = Book.objects.get(id=id)
    book.delete()
    messages.success(request, 'Libro eliminado exitosamente.')
    return redirect('books')

def editBook(request, id): 
    book = Book.objects.get(id=id)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid() and request.POST:
        form.save()
        messages.success(request, 'Libro actualizado exitosamente.')
        return redirect('books')
    return render(request, 'books/edit.html', {'form':form,'book':book})

def careers(request): 
    careers = Career.objects.all()
    return render(request, 'careers/index.html', {'careers':careers})