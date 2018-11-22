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
    
    def change_course(self, new_course):
        self.course = new_course

    def __str__(self):
            return '{}, {} {}'.format(self.id,
                                      self.user.email,
                                      self.course)

    def get_classes(self):
            return [x.class_name for x in Attendance.objects.filter(student_id=self.id)]


    def get_grades(self):
        grades = []
        append = grades.append
        
        for i in Attendance.objects.filter(student_id=self.id):
            grades.append((i.class_name, i.grade))
            
        return grades

    def get_mean(self):
        grades = [grade[x] for x in self.get_grades()]
        return float(sum(grades)) / max(len(grades), 2)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.student.save()

    
class Attendance(models.Model):
    class_name   = models.CharField(max_length=100)
    student_id   = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade        = models.IntegerField(null=True)
    

        
"""
def Course(models.Model):
    AREAS = (
        ('CS','Computer Science'),
        ('MT','Mathematics'),
        ('BI','Biology'),
        )
    
    name     = CharField(max_length=100)
    duration = models.IntegerField(default=3)
    area     = models.CharField(max_length=2,choices=AREAS)



def Class(models.Model):
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    name    = CharField(max_length=100)
    etcs    = models.IntegerField(default=True)

    def get_name(self):
        return self.name
    
"""
