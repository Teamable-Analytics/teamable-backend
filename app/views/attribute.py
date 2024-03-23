from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Attribute
from app.models.attribute import AttributeOption, AttributeResponse
from app.serializers.attribute import AttributeSerializer
from django.core.exceptions import FieldError, ObjectDoesNotExist


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course_id"]

    @staticmethod
    def clear_attribute_responses(attribute_id):
        num_attribute_responses_deleted, _ = AttributeResponse.objects.filter(
            attribute_option_id=attribute_id
        ).delete()
        return num_attribute_responses_deleted

    @action(detail=False, methods=["post"])
    def delete_student_responses(self, request):
        if "attribute_option_id" in request.data:
            if get_object_or_404(
                AttributeOption, pk=request.data["attribute_option_id"]
            ).has_student_responses:
                num_attribute_responses_deleted = self.clear_attribute_responses(
                    request.data["attribute_option_id"]
                )
            else:
                raise ObjectDoesNotExist(
                    "No student responses found for this attribute option"
                )
        else:
            raise FieldError("attribute_option_id field is required")
        return Response(f"{num_attribute_responses_deleted} responses deleted")
