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

    @action(detail=False, methods=["post"])
    def save_attribute(self, request):
        if "id" in request.data:
            attribute = get_object_or_404(Attribute, pk=request.data["id"])
            if request.data["value_type"] != attribute.value_type:
                # clear all student responses
                pass
            atribute_serializer = AttributeSerializer(attribute, data=request.data)
        else:
            atribute_serializer = AttributeSerializer(data=request.data)

        if atribute_serializer.is_valid():
            attribute = atribute_serializer.save()
        else:
            return Response(atribute_serializer.errors)

        if "options" in request.data:
            id_list_to_update = [
                option["id"] for option in request.data["options"] if "id" in option
            ]
            AttributeOption.objects.filter(attribute=attribute).exclude(
                id__in=id_list_to_update
            ).delete()

            for option in request.data["options"]:
                if "id" in option:
                    attribute_option = get_object_or_404(
                        AttributeOption, pk=option["id"]
                    )
                    attribute_option.label = option["label"]
                    attribute_option.value = option["value"]
                    attribute_option.save()
                else:
                    option["attribute"] = attribute.id
                    attribute_option_serializer = AttributeOptionSerializer(data=option)
                    if attribute_option_serializer.is_valid():
                        attribute_option_serializer.save()
                    else:
                        return Response(attribute_option_serializer.errors)

        return Response(atribute_serializer.data)
