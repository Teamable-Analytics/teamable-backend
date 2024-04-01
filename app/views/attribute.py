from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Attribute
from app.serializers.attribute import AttributeSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course_id"]

    @action(detail=False, methods=["post"])
    def delete_student_responses(self, request):
        attribute = get_object_or_404(Attribute, pk=request.data.get("attribute_id"))
        num_deleted_attribute_responses = attribute.delete_student_responses()
        return Response(
            {"num_deleted_attribute_responses": num_deleted_attribute_responses}
        )
