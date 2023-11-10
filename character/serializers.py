from rest_framework import serializers
from .models import ARace, AClass, Party, Adventurer,  BagItem


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'


class ARaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARace
        fields = '__all__'


class AClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = AClass
        fields = '__all__'


class BagItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BagItem
        fields = '__all__'

class HealthSerializer(serializers.Serializer):
    curr = serializers.IntegerField(source='healthcurrent')
    max = serializers.IntegerField(source='healthmax')

class LevelMetaSerializer(serializers.Serializer):
    level = serializers.IntegerField(source='level')
    exp = serializers.ReadOnlyField(default=0)
    nextlevel = serializers.ReadOnlyField(default=0)


class AdventurerSerializer(serializers.ModelSerializer):
    race = ARaceSerializer()
    aclass = AClassSerializer()
    nickname = serializers.SerializerMethodField()
    levelmeta = serializers.SerializerMethodField()
    calcstat = serializers.SerializerMethodField()
    health = serializers.SerializerMethodField()
    equipment = serializers.SerializerMethodField()
    bag = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    gold = serializers.SerializerMethodField()

    # Add other nested serializers or fields as required

    class Meta:
        model = Adventurer
        fields = [
            'name', 'nickname', 'race', 'aclass', 'levelmeta', 'calcstat',
            'health', 'money', 'origin', 'bag', 'equipment','gold','bio'
        ]

    def get_gold(self,obj):
        return obj.money

    def get_bio(self,obj):
        return obj.origin

    def get_bag(self,obj):
        return BagItemSerializer(obj.bagitem_set(),many=True).data

    def get_nickname(self,obj):
        return obj.subname


    def get_health(self,obj):
        return {
            "max":obj.collective.get('cns')*3 + obj.collective.get('str')*1,
            "curr":obj.health
        }

    def get_calcstat(self, obj):
        return obj.get_calcstat()


    def get_equipment(self,obj):
        return {"jajko":"kokosz"}

    def get_levelmeta(self,obj):
        return {"level":obj.level,"exp":obj.exp,"nextlevel": obj.getnextlevel}
