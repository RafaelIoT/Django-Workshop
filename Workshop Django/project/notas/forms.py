from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms

class Login(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', max_length=50)

class NewGrade(forms.Form):
    class_name = forms.CharField(label='Class', max_length=100)
    grade = forms.IntegerField(label='Grade',
                                  validators=[MinValueValidator(0),
                                              MaxValueValidator(20)]
                                  )
