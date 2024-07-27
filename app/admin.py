from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from app.models.attribute import Attribute, AttributeOption, AttributeResponse
from app.models.team import Team, TeamSet
from .models import CourseMember, Course, Section, Organization


class CourseMemberAdmin(admin.ModelAdmin):
    actions = ["create_jwt"]

    @admin.action(description="Create JWT token for selected course members")
    def create_jwt(self, request, queryset):
        data = {}
        for course_member in queryset:
            data[course_member.pk] = course_member.create_jwt_token()
        return JsonResponse(data)


# Register your models here.
admin.site.register(Course)
admin.site.register(Attribute)
admin.site.register(AttributeOption)
admin.site.register(AttributeResponse)
admin.site.register(Section)
admin.site.register(CourseMember, CourseMemberAdmin)
admin.site.register(Organization)
admin.site.register(TeamSet)
admin.site.register(Team)
