from dataclasses import field
from django import forms
from .models import Book, Career

class BookForm(forms.ModelForm): 
    class Meta:
        model = Book
        fields = '__all__'

class CareerForm(forms.ModelForm): 
    class Meta: 
        model = Career
        fields = '__all__'
