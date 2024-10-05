from django.contrib import admin
from django.http import JsonResponse

from app.models.attribute import Attribute, AttributeOption, AttributeResponse
from app.models.team import Team, TeamSet
from .models import CourseMember, Course, Section, Organization


class CourseMemberAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "course",
        "user",
        "role",
        "lms_id",
        "sis_user_id",
    ]
    actions = ["create_jwt"]

    @admin.action(description="Create JWT token for selected course members")
    def create_jwt(self, request, queryset):
        data = {}
        for course_member in queryset:
            data[course_member.pk] = course_member.create_jwt_token()
        return JsonResponse(data)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ["name", "course", "manage_type"]


class AttributeOptionAdmin(admin.ModelAdmin):
    list_display = ["id", "attribute", "label", "value", "course"]


class AttributeResponseAdmin(admin.ModelAdmin):
    list_display = ["id", "course_member", "attribute_option"]


class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "organization", "lms_course_id"]


class SectionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "course"]


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "lms_type"]


class TeamSetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "course"]


class TeamAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "name", "team_set"]


# Register your models here.
admin.site.register(Course, CourseAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeOption, AttributeOptionAdmin)
admin.site.register(AttributeResponse, AttributeResponseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(CourseMember, CourseMemberAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(TeamSet, TeamSetAdmin)
admin.site.register(Team, TeamAdmin)
