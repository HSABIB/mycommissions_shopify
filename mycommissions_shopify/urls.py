from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', include('landing.urls')),
    path('shopify/', include('xenon.urls')),
    path('api/', include('api.urls')),
]
