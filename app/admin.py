from django.contrib import admin

from app.models.attribute import Attribute, AttributeOption, AttributeResponse
from .models import CourseMember, Course, Section, Organization


# Register your models here.
admin.site.register(Course)
admin.site.register(Attribute)
admin.site.register(AttributeOption)
admin.site.register(AttributeResponse)
admin.site.register(Section)
admin.site.register(CourseMember)
admin.site.register(Organization)
