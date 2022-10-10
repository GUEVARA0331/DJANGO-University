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
    path('book/delete/<int:id>', views.deleteBook, name='deleteBook'),
    path('book/edit', views.editBook, name='editBook'),
    path('book/edit/<int:id>', views.editBook, name='editBook'),

    path('careers', views.careers, name='careers'),
    path('career/add', views.addCareer, name='addCareer'),
    path('career/edit', views.editCareer, name='editCareer'),
    path('career/edit/<int:id>', views.editCareer, name='editCareer'),
    path('career/delete/<int:id>', views.deleteCareer, name='deleteCareer'),
    path('career/consult/<name>', views.consultCareer, name='consultCareer'),
    
    path('students', views.students, name='students'),
    path('student/add', views.addStudent, name='addStudent'),
    path('student/edit', views.editStudent, name='editStudent'),
    path('student/edit/<int:id>', views.editStudent, name='editStudent'),
    path('student/delete/<int:id>', views.deleteStudent, name='deleteStudent'),

    path('courses', views.courses, name='courses'),
    path('course/add', views.addCourse, name='addCourse'),
    path('course/edit', views.editCourse, name='editCourse'),
    path('course/edit/<int:id>', views.editCourse, name='editCourse'),
    path('course/delete/<int:id>', views.deleteCourse, name='deleteCourse'),
    path('course/consult/<name>', views.consultCourse, name='consultCourse'),

    path('enrollments', views.enrollments, name='enrollments'),
    path('enrollment/add', views.addEnrollment, name='addEnrollment'),
    path('enrollmente/edit', views.editEnrollment, name='editEnrollment'),
    path('enrollmente/edit/<int:id>', views.editEnrollment, name='editEnrollment'),
    path('enrollment/delete/<int:id>', views.deleteEnrollment, name='deleteEnrollment'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)