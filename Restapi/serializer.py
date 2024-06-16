from rest_framework import serializers
from .models import register,combine

class registerserializer(serializers.ModelSerializer):
    class Meta:
        model=register
        fields='__all__'
        read_only_fields = ['user']

class combine_serializer(serializers.ModelSerializer):
    class Meta:
        model=combine
        fields='__all__'
        exclude='l_name'

from .models import user,profile,snippet
class methodserializer(serializers.ModelSerializer):
    user_detail=serializers.SerializerMethodField()

    class Meta:
        model=profile
        fields=["id","account_name","user_detail","created_at"]

    def get_user_detail(self,obj):
        users=obj.user.all()
        return [{
            "user":user.id,
            "name":user.name,
            "email":user.email,
        }for user in users]


class snippet_serializer(serializers.ModelSerializer):
    class Meta:
        model=snippet
        fields='__all__'

from .models import miscellance

class miscellanceserializer(serializers.ModelSerializer):
    read_only=serializers.ReadOnlyField(source='joined')

    class Meta:
        model=miscellance
        fields=["id","name","age","destinantion","read_only"]

from .models import Hiddenfield

class hiddenserializer(serializers.ModelSerializer):
    hidden=serializers.CharField(write_only=True)
    class Meta:
        model=Hiddenfield
        fields=["id","name","hidden"]

from .models import user_new
from django.utils.timezone import now
from datetime import datetime

class usernewserializer(serializers.ModelSerializer):
    date_since_joined=serializers.SerializerMethodField()
    summa_calculation=serializers.SerializerMethodField()
    class Meta:
        model=user_new
        fields=["user_name","age","email","date_joined","date_since_joined","summa_calculation"]

    def get_date_since_joined(self,obj):
        if obj.date_joined:
            return (datetime.now().date()-obj.date_joined).days
        else:
            return None

    def get_summa_calculation(self,obj):
        if (datetime.now().date()-obj.date_joined).days>0:
            return "positive"
        if (datetime.now().date()-obj.date_joined).days==0:
            return "today joined"
        else:
            return "negative"

from .models import studentdetails,schoolname


class studentserializer(serializers.ModelSerializer):
    school_name=serializers.SerializerMethodField()
    school_location=serializers.SerializerMethodField()
    class Meta:
        model=studentdetails
        fields=["name","age","school_name","school_location"]

    def get_school_name(self,obj):
        return obj.student_school.school_name

    def get_school_location(self,obj):
        return obj.student_school.school_location



class sourceserializer(serializers.ModelSerializer):
    school_name=serializers.CharField(source="student_school.school_name",read_only=True)
    school_location=serializers.CharField(source="student_school.school_location",read_only=True)
    living=serializers.SerializerMethodField(method_name="calculate_custom")
    class Meta:
        model=studentdetails
        fields=["name","age","school_name","school_location","living"]

    def calculate_custom(self,obj):
        return 5


































