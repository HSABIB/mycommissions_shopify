from django.urls import path

import xenon.views as views

urlpatterns = [
    path('authenticate/', views.authenticate_shopify, name='shopify_app_authenticate'),
    path('finalize/', views.finalize, name='shopify_app_login_finalize'),
]
