from django.db.models import Avg, F
from rest_framework import serializers
from .models import pcc


class querychainingserializer(serializers.ModelSerializer):
    player = serializers.CharField(source="youngest_player_team.young_player.player", read_only=True)

    class Meta:
        model = pcc
        fields = ["captain", "player"]


from .models import employess


class employeesserializer(serializers.ModelSerializer):
    class Meta:
        model = employess
        fields = '__all__'


from .models import organization, companys


class somethingserializer(serializers.ModelSerializer):
    # org_name=serializers.CharField(source='company_org_name.org_name',read_only=True)
    org_name = serializers.SerializerMethodField()
    org_location = serializers.SerializerMethodField()
    average_salary = serializers.SerializerMethodField()

    class Meta:
        model = companys
        fields = ["company_name", "company_owner", "org_name", "org_location", "average_salary"]

    def get_org_location(self, obj):
        return obj.company_org_name.org_location

    def get_org_name(self, obj):
        return obj.company_org_name.org_name

    def get_average_salary(self, obj):
        avg = employess.objects.filter(emp_company_name=obj).aggregate(avgsalary=Avg("emp_salary"))["avgsalary"]

        return avg
