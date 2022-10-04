from dataclasses import field
from django import forms
from .models import Book, Career, Course, Student

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

class StudentForm(forms.ModelForm): 
    class Meta: 
        model = Student
        fields = '__all__'
        widgets = {
            'dateBirth': forms.DateInput(attrs={'type': 'date'}),
            'sex': forms.Select(attrs={'class':'form-control'}),
            'career': forms.Select(attrs={'class':'form-control'})
        }