from django.forms import ValidationError
from django.core.exceptions import FieldError
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.models import Attribute
from app.models.attribute import AttributeOption
from app.serializers.attribute import AttributeOptionSerializer, AttributeSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course_id"]

    @staticmethod
    def clear_student_responses():
        pass

    @staticmethod
    def delete_attribute_options_not_in_list(attribute, attribute_options):
        attribute_options_id_list = [
            option["id"] for option in attribute_options if "id" in option
        ]
        AttributeOption.objects.filter(attribute=attribute).exclude(
            id__in=attribute_options_id_list
        ).delete()

        return attribute_options_id_list

    @staticmethod
    def save_attribute_option(option):
        if "id" in option:
            attribute_option = get_object_or_404(AttributeOption, pk=option["id"])
            attribute_option_serializer = AttributeOptionSerializer(
                attribute_option, data=option
            )
        else:
            attribute_option_serializer = AttributeOptionSerializer(data=option)

        if attribute_option_serializer.is_valid():
            attribute_option = attribute_option_serializer.save()
        else:
            raise ValidationError("Invalid attribute option")

        return attribute_option

    @action(detail=False, methods=["post"])
    def save_attribute(self, request):
        if "id" in request.data:
            attribute = get_object_or_404(Attribute, pk=request.data["id"])
            if request.data["value_type"] != attribute.value_type:
                self.clear_student_responses()
            attribute_serializer = AttributeSerializer(attribute, data=request.data)
        else:
            attribute_serializer = AttributeSerializer(data=request.data)

        if attribute_serializer.is_valid():
            attribute = attribute_serializer.save()
        else:
            return Response(attribute_serializer.errors)

        if "options" in request.data:
            self.delete_attribute_options_not_in_list(
                attribute, request.data["options"]
            )

            for option in request.data["options"]:
                option["attribute"] = attribute.id
                self.save_attribute_option(option)
        else:
            raise FieldError("Options field is required")

        return Response(attribute_serializer.data)
