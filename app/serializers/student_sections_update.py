from rest_framework import serializers
from app.models.section import Section
from app.models.course import Course  # Assuming you have a Course model

class StudentSectionsUpdateSerializer(serializers.Serializer):
    sections = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        error_messages={"required": "Sections is required.", "invalid": "Sections must be a list of integers."},
    )

    def validate_sections(self, value):
        if not all(isinstance(section_id, int) for section_id in value):
            raise serializers.ValidationError("Sections must be a list of integers.")

        course = self.context.get('course')

        course_sections_ids = Section.objects.filter(course=course).values_list('id', flat=True)
        if not all(section_id in course_sections_ids for section_id in value):
            raise serializers.ValidationError("One or more sections do not exist or are not part of the course.")
        return value

    def update(self, instance, validated_data):
        section_ids = validated_data["sections"]
        sections = Section.objects.filter(id__in=section_ids)
        instance.sections.set(sections)
        return instance
