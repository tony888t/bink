from django.urls import path

from . import views


urlpatterns = [
    path('', views.get_operation, name='phone_mast'),
    path('current-rent', views.sort_by_current_rent, name='sort_current_rent')
]
