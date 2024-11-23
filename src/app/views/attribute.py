from django.forms import ValidationError
from django.core.exceptions import FieldError
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

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
    def delete_student_responses(self, request):
        attribute = get_object_or_404(Attribute, pk=request.data.get("attribute_id"))
        num_deleted_attribute_responses = attribute.delete_student_responses()
        return Response(
            {"num_deleted_attribute_responses": num_deleted_attribute_responses}
        )
