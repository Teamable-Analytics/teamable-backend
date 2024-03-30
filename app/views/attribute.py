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

    @action(detail=False, methods=["post"])
    def delete_student_responses(self, request):
        if "attribute_id" in request.data:
            attribute = get_object_or_404(Attribute, pk=request.data["attribute_id"])
            print(AttributeOption.objects.all().values_list("attribute_id", flat=True))
            return Response(attribute.num_student_responses)
        return Response("Hello, World!")
    
    # @action(detail=False, methods=["post"])
    # def delete_student_responses(self, request):
    #     if "attribute_option_id" in request.data:
    #         attribute_option = get_object_or_404(AttributeOption, pk=request.data["attribute_option_id"])
    #         if attribute_option.has_student_responses:
    #             num_attribute_responses_deleted = AttributeResponse.clear_attribute_responses(
    #                 request.data["attribute_option_id"]
    #             )
    #         else:
    #             raise ObjectDoesNotExist(
    #                 "No student responses found for this attribute option"
    #             )
    #     else:
    #         raise FieldError("attribute_option_id field is required")
    #     return Response({num_attribute_responses_deleted: num_attribute_responses_deleted, attribute_id: attribute_option_id})
