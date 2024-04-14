from rest_framework import serializers

from accounts.serializers import MyUserSerializer
from app.models.course_member import CourseMember
from app.serializers.attribute import AttributeResponseSerializer
from app.serializers.relationship import RelationshipSerializer
from app.serializers.section import SectionSerializer
from app.models.section import Section


class CourseMemberSerializer(serializers.ModelSerializer):
    outbound_relationships = RelationshipSerializer(
        "outbound_relationships", many=True, read_only=True
    )
    attribute_responses = AttributeResponseSerializer(
        "attribute_responses", many=True, read_only=True
    )

    user = MyUserSerializer(read_only=True)
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = CourseMember
        fields = "__all__"


class UpdateStudentSectionsRequest(serializers.Serializer):
    sections = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        error_messages={
            "required": "Sections is required.",
            "invalid": "Sections must be a list of integers.",
        },
    )

    def validate_sections(self, value):
        course = self.context.get("course")
        sections_passed_in = set(value)
        course_sections_ids = Section.objects.filter(
            course=course, id__in=sections_passed_in
        )
        if len(sections_passed_in) != course_sections_ids.count():
            raise serializers.ValidationError(
                "One or more sections do not exist or are not part of the course."
            )
        return value
