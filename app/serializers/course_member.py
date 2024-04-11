from rest_framework import serializers

from accounts.serializers import MyUserSerializer
from app.models.course_member import CourseMember
from app.serializers.attribute import AttributeResponseSerializer
from app.serializers.relationship import RelationshipSerializer
from app.serializers.section import SectionSerializer


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
