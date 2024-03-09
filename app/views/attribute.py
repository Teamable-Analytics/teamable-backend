from rest_framework.response import Response
from rest_framework import viewsets, status

from app.models import Attribute
from app.serializers.attribute import AttributeSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = []

    def list(self, request):
        course_id = request.GET.get('course_id', None)
        query_set = self.filter_queryset(self.get_queryset())

        if course_id:
            query_set = query_set.filter(course_id=course_id)
        else:
            return Response("course_id is required", status=status.HTTP_400_BAD_REQUEST)

        serializer = AttributeSerializer(query_set, many=True)
        return Response(serializer.data)
