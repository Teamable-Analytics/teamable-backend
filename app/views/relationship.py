from rest_framework import viewsets

from app.models.relationship import Relationship
from app.serializers.relationship import RelationshipSerializer


class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
