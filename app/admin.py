from django.contrib import admin
from .models import CourseMember
from .models import Course
from .models import Section


# Register your models here.
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(CourseMember)
