from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from character.views import AdventurerViewSet

z=SimpleRouter()
z.register('advs',AdventurerViewSet,basename="jajar")

urlpatterns = [
] + z.urls


websocket_urlpatterns = [

]