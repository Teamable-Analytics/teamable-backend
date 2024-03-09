from rest_framework import viewsets
from django_filters import rest_framework as filters

from app.models import Attribute
from app.serializers.attribute import AttributeSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course_id"]
