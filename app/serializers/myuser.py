from rest_framework import serializers
from accounts.models import MyUser
from app.models.section import Section
from app.models.course_member import CourseMember

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'first_name', 'last_name']  

# Serializer for the Section model
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name'] 
