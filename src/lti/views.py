from django.urls import reverse
from pylti1p3.contrib.django import DjangoOIDCLogin, DjangoMessageLaunch
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.authtoken.models import Token

from accounts.models import MyUser
from app.models import CourseMember, Course, Organization
from app.models.course_member import UserRole
from lti import lti_util
from pprint import pprint


# do not require deployments in config
class ExtendedDjangoMessageLaunch(DjangoMessageLaunch):
    def validate_deployment(self):
        return self


@csrf_exempt
def login(request):
    if not settings.LTI_ENABLED:
        raise Exception("LTI disabled")

    # clear old sessions (just to be safe)
    auth_logout(request)

    tool_conf = lti_util.get_tool_conf()
    oidc_login = DjangoOIDCLogin(request, tool_conf)

    target_link_uri = request.POST.get(
        "target_link_uri", request.GET.get("target_link_uri")
    )
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')

    return oidc_login.redirect(target_link_uri)


@csrf_exempt
@require_POST
def launch(request):
    if not settings.LTI_ENABLED:
        raise Exception("LTI disabled")

    tool_conf = lti_util.get_tool_conf()
    message_launch = ExtendedDjangoMessageLaunch(request, tool_conf)

    message_launch_data = message_launch.get_launch_data()

    # check if instructor (only instructors can LTI launch at this time)
    roles = message_launch_data.get("https://purl.imsglobal.org/spec/lti/claim/roles")
    has_admin_role = (
        "http://purl.imsglobal.org/vocab/lis/v2/membership#Administrator" in roles
    )
    has_content_developer_role = (
        "http://purl.imsglobal.org/vocab/lis/v2/membership#ContentDeveloper" in roles
    )
    has_instructor_role = (
        "http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor" in roles
    )
    has_ta_role = (
        "http://purl.imsglobal.org/vocab/lis/v2/membership/Instructor#TeachingAssistant"
        in roles
    )

    role = UserRole.STUDENT
    if has_admin_role:
        role = UserRole.INSTRUCTOR
    elif has_content_developer_role:
        role = UserRole.INSTRUCTOR
    elif has_instructor_role and not has_ta_role:
        role = UserRole.INSTRUCTOR
    elif has_ta_role:
        role = UserRole.INSTRUCTOR

    if settings.DEBUG:
        pprint(message_launch_data)

    launch_iss = message_launch_data.get("iss")

    # create/sync user
    # custom variables need to be defined in Canvas, defined by consulting
    #   https://gist.github.com/jbasdf/15fb8abed66fbaf623cdfbdd45bfb1c4
    canvas_course_id = message_launch_data.get(
        "https://purl.imsglobal.org/spec/lti/claim/custom", {}
    ).get("canvas_course_id")
    canvas_user_id = message_launch_data.get(
        "https://purl.imsglobal.org/spec/lti/claim/custom", {}
    ).get("canvas_user_id")

    auth_user, created = MyUser.objects.get_or_create(
        # Make the username unique to the launch ISS, so different
        # institution's Canvas instance creates unique usernames
        username=f"{canvas_user_id}+{launch_iss}"
    )
    auth_user.first_name = message_launch_data.get("given_name")
    auth_user.last_name = message_launch_data.get("family_name")

    auth_user.set_unusable_password()
    auth_user.save()

    auth_user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, auth_user)

    # make the authentication token for the frontend
    Token.objects.get_or_create(user=auth_user)

    # todo: this is only true for now
    organization = Organization.objects.first()

    course, created = Course.objects.get_or_create(
        lms_course_id=canvas_course_id,
        defaults={
            "name": message_launch_data.get(
                "https://purl.imsglobal.org/spec/lti/claim/context", {}
            ).get("label"),
            "organization": organization,
        },
    )

    course_member, created = CourseMember.objects.get_or_create(
        user=auth_user,
        course=course,
        defaults={
            "first_name": auth_user.first_name,
            "last_name": auth_user.last_name,
            "lms_id": canvas_user_id,
        },
    )
    course_member.role = role
    course_member.save()

    return redirect(
        f"{reverse('canvas-oauth-initiate')}?redirect_path=/course/{course.id}"
    )
