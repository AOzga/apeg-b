
from django.contrib import admin
from django.urls import path,include

import testfetch
from srv.rootcons import TestConsumer
from auth import urls as asaurla

ulra = [

    path('char/',include('character.urls')),
    path('event/',include('events.urls')),
    path('map/',include('map.urls')),
    path('npc/',include('npc.urls')),
]
urlpatterns=[
    path('api/',include(ulra)),
    path('api/v2/',include(asaurla))
]




websocket_urlpatterns = [
    path('endws/',TestConsumer.as_asgi())
]