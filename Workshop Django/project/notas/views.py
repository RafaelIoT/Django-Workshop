from django.shortcuts               import render, redirect
from django.http                    import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth            import authenticate, login
from django.template.defaulttags    import register
from django.contrib.auth.models     import User
from django.views.decorators.csrf   import csrf_exempt
from .forms                         import Login, NewGrade
from .models                        import *

def login_user(request):
    if request.method == 'POST':
        form = Login(request.POST)

        if form.is_valid():
            EMAIL    = request.POST['email']
            USERNAME = request.POST['username']
            PASSWORD = request.POST['password']
            
            user = authenticate(email=EMAIL, username=USERNAME, password=PASSWORD)

            if user is not None:
                print('USER NOT NONE')
                login(request, user)
                return HttpResponseRedirect('/notas/home')
            else:
                print('error 1')
                form = Login()
                return render(request,
                              'notas/form.html',
                              {'form': form,
                               'response':'invalid password'})

    else:
        form = Login()
    form = Login()
    print('error 2')
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



def get_mean(request):
    if request.user.is_authenticated:
        grades = []
        for grade in Attendance.objects.filter(student_id = request.user.student.id):
            grades.append((grade.grade))

        student_mean = str(round(float(sum(grades)/len(grades)),2))
        return JsonResponse({'mean':student_mean})
    else:
        form = Login()
        return render(request, 'notas/login.html',{'form': form})



def add_grade(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            new_grade = NewGrade(request.POST)
            if new_grade.is_valid():
                print(request.POST)
                class_name = request.POST['class_name']
                grade = request.POST['grade']
                Attendance(
                    class_name=class_name, 
                    grade=grade, 
                    student_id=request.user.student
                      ).save()
            print('OK')
            return HttpResponseRedirect('/notas/home')
        else:
            gradeForm = NewGrade()
            data = {
                'user':request.user,
                'grades': grades,
                'form':gradeForm, 
                'error':new_grade.errors
                }

            return render(request, 'notas/home.html', data)
    else:
        form = Login()
        return render(request, 'prt/form.html',{'form': form})




@register.filter
def get_first(list):
        return list[0]

@register.filter
def get_second(list):
        return list[1]

    
			
