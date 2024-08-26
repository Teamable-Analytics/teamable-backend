from rest_framework.decorators import action

from accounts.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    MyUserSerializer,
)
from rest_framework import viewsets, serializers
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from accounts.models import MyUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], serializer_class=serializers.Serializer)
    def me(self, request, pk=None):
        serializer = MyUserSerializer(request.user)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = MyUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UserLoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserLoginSerializer
    queryset = MyUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
