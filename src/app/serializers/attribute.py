from rest_framework import serializers

from app.models import Attribute, AttributeResponse, AttributeOption


class AttributeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeOption
        fields = "__all__"


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["id", "name"]


class AttributeResponseSerializer(serializers.ModelSerializer):
    attribute_option = AttributeOptionSerializer(read_only=True)

    class Meta:
        model = AttributeResponse
        fields = "__all__"
