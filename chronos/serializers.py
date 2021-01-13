from rest_framework import serializers
from .models import Group, Course

class GroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = Group
    fields = ('name', 'entity_id', 'date_added')

class CourseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Course
    fields = ('title', 'date_added')