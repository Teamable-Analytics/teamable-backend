from django.forms import ValidationError
from django.core.exceptions import FieldError
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.models import Attribute
from app.models.attribute import AttributeOption
from app.models.course import Course
from app.serializers.attribute import AttributeOptionSerializer, AttributeSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course_id"]

    def save_attribute_option(
        self, attribute_option_data: dict, attribute_id: int
    ) -> AttributeOption:
        attribute_option_serializer = AttributeOptionSerializer(
            data={**attribute_option_data, "attribute": attribute_id}
        )
        if not attribute_option_serializer.is_valid():
            raise ValidationError(attribute_option_serializer.errors)
        attribute = get_object_or_404(Attribute, pk=attribute_id)

        attribute_option_id = attribute_option_data.get("id")
        if attribute_option_id:
            attribute_option = get_object_or_404(
                AttributeOption, pk=attribute_option_id
            )
            AttributeOption.objects.filter(pk=attribute_option_id).update(
                **{**attribute_option_data, "attribute": attribute}
            )
        else:
            attribute_option = AttributeOption.objects.create(
                **{**attribute_option_data, "attribute": attribute}
            )

        return attribute_option

    @action(detail=False, methods=["post"])
    def save_attribute(self, request):
        attribute_serializer = AttributeSerializer(data=request.data)
        if not attribute_serializer.is_valid():
            raise ValidationError(attribute_serializer.errors)

        course = get_object_or_404(Course, pk=request.data.get("course"))

        attribute_id = request.data.get("id")
        if attribute_id:
            attribute = get_object_or_404(Attribute, pk=request.data.get("id"))
            if (
                request.data.get("value_type") != attribute.value_type
                or request.data.get("max_selections") < attribute.max_selections
            ):
                attribute.clear_student_responses()

            Attribute.objects.filter(pk=attribute_id).update(
                **{**attribute_serializer.data, "course": course}
            )
        else:
            attribute = Attribute.objects.create(
                **{**attribute_serializer.data, "course": course}
            )

        attribute_options = request.data.get("options")
        if attribute_options is not None:
            for attribute_option in attribute_options:
                self.save_attribute_option(attribute_option, attribute.id)
        else:
            raise FieldError("Options field is required")

        return Response({"data": AttributeSerializer(attribute).data})
