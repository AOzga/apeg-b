from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from character.models import AClass, ARace
from character.serializers import AdventurerSerializer


class AdventurerViewSet(GenericViewSet):
    @action(detail=False, methods=['get'], name='fetchraces')
    def fetchrace(self, request: Request):
        return Response(data=[{"id":a.id,"name":a.name,"racestat":a.rstat} for a in ARace.objects.all()])

    @action(detail=False, methods=['get'], name='fetchclass')
    def fetchclass(self, request: Request):
        return Response(data=[{"id":a.id,"name":a.name,"mainstat":a.mstat,"substat":a.sstat} for a in AClass.objects.all()])

    @action(detail=False, methods=['get'], name='getchar')
    def getchar(self, request: Request):
        return Response(AdventurerSerializer(request.user.adventurer).data)

    @action(detail=False,methods=['post'],name='setchar')
    def setchar(self,request:Request):
        user = request.user
        user.adventurer.name = request.data.get('name')
        user.adventurer.subname = request.data.get('nickname')
        user.adventurer.aclass = request.data.get('class')
        user.adventurer.race = request.data.get('race')
        user.adventurer.origin = request.data.get('bio')
        user.adventurer.save()
        return Response(AdventurerSerializer(request.user.adventurer).data)
