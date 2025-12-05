from django.urls import path

from . import views

app_name = 'transactional_system_core'

urlpatterns = [
    path('transfer', views.create_transfer)
]