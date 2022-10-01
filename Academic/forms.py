from dataclasses import field
from django import forms
from .models import Book, Career, Course

class BookForm(forms.ModelForm): 
    class Meta:
        model = Book
        fields = '__all__'

class CareerForm(forms.ModelForm): 
    class Meta: 
        model = Career
        fields = '__all__'

class CourseForm(forms.ModelForm): 
    class Meta: 
        model = Course
        fields = '__all__'