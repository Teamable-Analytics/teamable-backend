from rest_framework import viewsets

from app.models import Attribute
from app.serializers.attribute import AttributeSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
