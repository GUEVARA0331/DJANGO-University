from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPAuthenticationError
from socket import gaierror

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