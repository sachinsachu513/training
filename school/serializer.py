from rest_framework import serializers
from .models import StudentName,School

class StudentSerializer(serializers.ModelSerializer):
      school_name=serializers.SerializerMethodField()
      school_location=serializers.SerializerMethodField()

      class Meta:
          model=StudentName
          fields='__all__'

      def get_school_name(self,obj):
          return obj.school.name
      def get_school_location(self,obj):
          return obj.school.location
class schoolserializer(serializers.ModelSerializer):
    class Meta:
        model=School
        fields='__all__'







