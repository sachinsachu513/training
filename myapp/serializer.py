from rest_framework import serializers
from .models import pcc
class querychainingserializer(serializers.ModelSerializer):
    player=serializers.CharField(source="youngest_player_team.young_player.player",read_only=True)
    class Meta:
        model=pcc
        fields=["captain","player"]

from .models import employess

class employeesserializer(serializers.ModelSerializer):
    class Meta:
        model=employess
        fields='__all__'
