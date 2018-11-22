# Django-Workshop

### First create virtualenv
$ pip install virtualenvwrapper-win

$ mkvirtualenv project

$ workon project

### Intall Django
pip install Django

### Then create a new Django project
$ django-admin startproject project

project /
manage.py
    project /
        __init__.py
        settings.py
        urls.py
        wsgi.py



### Start a new app
$ python manage.py startapp notas

project/
    notas/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
        models.py
        tests.py
        views.py


### Add new app to settings.py INSTALLED_APPS

### Go to project urls.py and add a new path to your app
urlpatterns = [
    *** path('notas/', include('notas.urls')), ***
    path('admin/', admin.site.urls),
]

## Write Models
```
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save

class Student(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    course   = models.CharField(max_length=100)
    late     = models.BooleanField(default=False)
    enrolled = models.IntegerField(default=2018)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.student.save()

class Attendance(models.Model):
    class_name  = models.CharField(max_length=100)
    student_id  = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade       = models.IntegerField(null=True)
    
```

### the Admin page
$ python manage.py createsuperuser

Open admin.py and register models to show them on admin
```
from django.contrib import admin
from .models import *

class StudentAdmin(admin.ModelAdmin):
    pass

class AttendanceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)

```

### Make migrations 
$ python manage.py makemigrations notas
> By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve > made new ones) and that you’d like the changes to be stored as a migration.

$ python manage.py migrate
> the migrate command takes all the migrations that haven’t been applied (Django tracks which ones are applied using > a special table in your database called django_migrations) and runs them against your database - essentially, 
> synchronizing the changes you made to your models with the schema in the database.

### Get sql
$ python manage.py sqlmigrate notas 0001

### Django shell
$ pyhton manage.py shell
>>> from notas.models import *
>>> from django.contrib.auth.models import User
>>> u = User.objects.create_user('rvc', 'fc50380@alunos.fc.ul.pt', 'rvc123')
>>> u.save()
>>> User.objects.all()
>>> user.student


## Write views
```
def login_user(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            EMAIL    = request.POST['email']
            USERNAME = request.POST['username']
            PASSWORD = request.POST['password']   
            user = authenticate(email=EMAIL, username=USERNAME, password=PASSWORD)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/notas/home')
            else:
                form = Login()
                return render(request,'notas/form.html',{'form': form,'response':'invalid password'})
    else:
        form = Login()
    form = Login()
    return render(request, 'notas/form.html',{'form': form})

            

def home(request):
    if request.user.is_authenticated:
        grades =[]
        student_attendance = Attendance.objects.filter(student_id = request.user.student.id)
        append = grades.append
        [append((c.class_name, c.grade)) for c in student_attendance]
        gradeForm = NewGrade()
        data = {'user':request.user,'grades': grades, 'form':gradeForm}
        return render(request, 'notas/home.html', data)
    else:
        form = Login()
        return render(request, 'notas/login.html',{'form': form})
```

## Write Forms 
```
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
```

### Models filters
>>> Attendace.objects.filter(class_name='CSS')
>>> Attendace.objects.filter(class_name='CSS', grade=20)
>>> Attendace.objects.filter(class_name='CSS', grade__lt=20)
>>> Attendace.objects.filter(class_name='CSS', grade__lte=20)
>>> Attendace.objects.filter(grade__lte=20, grade_gt=16)
>>> Attendance.objects.order_by('grade')
>>> Attendance.objects.filter(class_name__contains='P')

### Complex queries
from django.db.models import Q
>>> Attendance.objects.filter(Q(grade=20) | ~Q(grade=16))
>>> Attendance.objects.filter(Q(grade=20) | ~Q(grade=16))

## Templates
```
return render(request, 'notas/home.html', {'variable_sent_by_view':'Hello'})
```
```
{% load static from staticfiles %}
{% csrf_token %}

{{ variable_sent_by_view }}

{% if variable_sent_by_view %}
    {{ variable_sent_by_view }}
{% endif %}

{% for i in list_sent_by_view %}
    {{ i }}
{% endfor %}

{% for i in list_sent_by_view %}
    <li> {{ i|get_first }} , {{ i|get_second}} </li>
{% endfor %}
```

### 
@register.filter
def get_first(list):
        return list[0]

@register.filter
def get_second(list):
        return list[1]
