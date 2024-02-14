from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=500)
    url = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    start_date = models.  DateTimeField(null=    True)
    end_date = models.DateTimeField(null=True)









class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
