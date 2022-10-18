from multiprocessing import context
from re import template
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPAuthenticationError
from socket import gaierror
from .models import Book, Career, Student, Course, Enrollment
from .forms import BookForm, CareerForm, CourseForm, StudentForm, EnrollmentForm
from django.conf import settings 
from django.db.models import Prefetch, Count

""" Imports to pdf """
from django.views import View
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

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
    books = Book.objects.all().order_by('-id')
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

def consultBook(request, title): 
    books = Book.objects.filter(title__icontains=title)
    return render(request, 'books/ajax/consult.html', {'books':books})

def editBook(request, id): 
    book = Book.objects.get(id=id)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid() and request.POST:
        """ 
            if len(request.FILES) != 0:
            if len(book.image) > 0:
                oldBook = Book.objects.get(id=id)
                os.remove(oldBook.image.name) 
        """
        form.save()
        messages.success(request, 'Libro actualizado exitosamente.')
        return redirect('books')
    return render(request, 'books/edit.html', {'form':form,'book':book})

def careers(request): 
    careers = Career.objects.all().annotate(students=Count('student')).order_by('-id')
    return render(request, 'careers/index.html', {'careers':careers})

def addCareer(request): 
    form = CareerForm(request.POST or None)
    if form.is_valid(): 
        form.save()
        messages.success(request, 'Carrera registrada exitosamente.')
        return redirect('careers')
    return render(request, 'careers/add.html', {'form':form})

def editCareer(request, id): 
    career = Career.objects.get(id=id)
    form = CareerForm(request.POST or None, instance=career)
    if form.is_valid() and request.POST: 
        form.save()
        messages.success(request, 'Carrera actualizada exitosamente.')
        return redirect('careers')
    return render(request, 'careers/edit.html', {'form':form})

def deleteCareer(request, id): 
    career = Career.objects.get(id=id)
    career.delete()
    messages.success(request, 'Carrera eliminada exitosamente')
    return redirect('careers')

def consultCareer(request, name): 
    careers = Career.objects.filter(name__icontains=name).annotate(students=Count('student'))
    return render(request, 'careers/ajax/consult.html', {'careers':careers})

class ExportPDFCareers(View): 
    def link_callback(self, uri, rel, type):
        """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
            Installation: pip install xhtml2pdf
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
        else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        template = get_template('careers/report.html')
        context = {
            'careers': Career.objects.all().annotate(students=Count('student')).order_by('name'),
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
        if pisaStatus.err:
            return HttpResponse('Se ha presentado un error al genera el reporte.')
        return response

def students(request): 
    students = Student.objects.all().order_by('-id')
    return render(request, 'students/index.html', {'students':students})

def addStudent(request): 
    form = StudentForm(request.POST or None)
    if form.is_valid(): 
        form.save()
        messages.success(request, 'Estudiante registrado exitosamente.')
        return redirect('students')
    return render(request, 'students/add.html', {'form':form})

def editStudent(request, id): 
    student = Student.objects.get(id=id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid() and request.POST: 
        form.save()
        messages.success(request, 'Estudiante actualizado existosamente')
        return redirect('students')
    return render(request, 'students/edit.html', {'form':form})

def deleteStudent(request, id): 
    student = Student.objects.get(id=id)
    student.delete()
    messages.success(request, 'Estudiante elimando exitosamente')
    return redirect('students')

def consultStudent(request, identification): 
    students = Student.objects.filter(identification__icontains=identification)
    return render(request, 'students/ajax/consult.html', {'students':students})

def courses(request): 
    courses = Course.objects.all().annotate(enrollments=Count('enrollment')).order_by('-id')
    return render(request, 'courses/index.html', {'courses':courses})

def addCourse(request): 
    form = CourseForm(request.POST or None)
    if form.is_valid(): 
        form.save()
        messages.success(request, 'Curso registrado exitosamente.')
        return redirect('courses')
    return render(request, 'courses/add.html', {'form':form})

def editCourse(request, id): 
    course = Course.objects.get(id=id)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid() and request.POST: 
        form.save()
        messages.success(request, 'Curso actualizado exitosamente.')
        return redirect('courses')
    return render(request, 'courses/edit.html', {'form':form})

def deleteCourse(request, id): 
    course = Course.objects.get(id=id)
    course.delete()
    messages.success(request, 'Curso eliminado exitosamente.')
    return redirect('courses')

def consultCourse(request, name): 
    courses = Course.objects.filter(name__icontains=name).annotate(enrollments=Count('enrollment'))
    return render(request, 'courses/ajax/consult.html', {'courses':courses})

def enrollments(request): 
    enrollments = Enrollment.objects.all().order_by('-id')
    return render(request, 'enrollments/index.html', {'enrollments':enrollments})

def addEnrollment(request): 
    form = EnrollmentForm(request.POST or None)
    if form.is_valid(): 
        form.save()
        messages.success(request, 'Matricula registrada exitosamente.')
        return redirect('enrollments')
    return render(request, 'enrollments/add.html', {'form':form})

def editEnrollment(request, id):  
    enrollment = Enrollment.objects.get(id=id)
    form = EnrollmentForm(request.POST or None, instance=enrollment)
    if form.is_valid() and request.POST: 
        form.save()
        messages.success(request, 'Matricula actualizada exitosamente.')
        return redirect('enrollments')
    return render(request, 'enrollments/edit.html', {'form':form})

def deleteEnrollment(request, id): 
    enrollment = Enrollment.objects.get(id=id)
    enrollment.delete()
    messages.success(request, 'Matricula eliminada exitosamente.')
    return redirect('enrollments')

def consultEnrollments(request, identification): 
    enrollments = Enrollment.objects.all().prefetch_related(Prefetch('student', queryset=Student.objects.filter(identification__icontains=identification))).filter(student__identification__icontains=identification)
    return render(request, 'enrollments/ajax/consult.html', {'enrollments':enrollments})
    









