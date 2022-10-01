from email.policy import default
from enum import unique
from random import choices
from weakref import proxy
from django.db import models

# Create your models here.
class Career(models.Model): 
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=8, verbose_name="Código", unique=True)
    name = models.CharField(max_length=50, verbose_name="Nombre")
    duration = models.PositiveSmallIntegerField(default=5, verbose_name="Duración (años)")

    class Meta: 
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"

    def __str__(self):
        txt = "{0} ({1} año(s))"
        return txt.format(self.name, self.duration)

class Student(models.Model): 
    id = models.AutoField(primary_key=True)
    identification = models.CharField(max_length=10, verbose_name="Identificación", unique=True)
    paternalSurname = models.CharField(max_length=35, verbose_name="Apellido paterno")
    maternalSurname = models.CharField(max_length=35, verbose_name="Apellido materno")
    names = models.CharField(max_length=35, verbose_name="Nombres")
    dateBirth = models.DateField(verbose_name="Fecha de nacimento")
    sexes = [('F','Femenino'),('M','Masculino')]
    sex = models.CharField(max_length=1, choices=sexes, default='F', verbose_name="Sexo")
    career = models.ForeignKey(Career, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Carrera")
    validity = models.BooleanField(default=True, verbose_name="Vigencia")

    def fullName(self): 
        txt = "{0} {1} {2}"
        return txt.format(self.paternalSurname, self.maternalSurname, self.names)

    class Meta: 
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self): 
        txt = "{0} - {1} ({2})"
        if self.validity: 
            studentStatus = "VIGENTE"
        else: 
            studentStatus = "DE BAJA"
        return txt.format(self.fullName(), self.career, studentStatus)

class Course(models.Model): 
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=8, verbose_name="Código", unique=True)
    name = models.CharField(max_length=30, verbose_name="Nombre")
    credits = models.PositiveSmallIntegerField(verbose_name="Créditos")
    professor = models.CharField(max_length=100, verbose_name="Docente")

    class Meta: 
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self): 
        txt = "{0} ({1}) - Docente: {2}"
        return txt.format(self.name, self.code, self.professor)

class Enrollment(models.Model): 
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Estudiante")
    course = models.ForeignKey(Course, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Curso")
    enrollmentDate = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de matriculación")

    class Meta: 
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"

    def __str__(self): 
        txt = "{0}: matriculad{1} en el curso {2} / Fecha: {3}"
        if self.student.sex == 'F': 
            sexLetter = "a"
        else:
            sexLetter = "o"
        enrDat = self.enrollmentDate.strftime("%A %d/%m/%Y %H:%M:%S")
        return txt.format(self.student.fullName(), sexLetter, self.course, self.enrollmentDate)

class Book(models.Model): 
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Título")
    image = models.ImageField(upload_to='images/', null=True, verbose_name="Imagen")
    description = models.TextField(null=True, verbose_name="Descripción")

    class Meta: 
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def __str__(self): 
        txt = "Título {0} - Descripción: {1}"
        return txt.format(self.title, self.description)

    def delete(self, using=None, keep_parents=False): 
        self.image.storage.delete(self.image.name)
        super().delete()


