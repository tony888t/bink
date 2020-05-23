from django.urls import path

from . import views


urlpatterns = [
    path('', views.get_operation, name='phone_mast'),
    path('current-rent', views.sort_by_current_rent, name='sort_current_rent'),
    path('filter-lease', views.filter_by_lease, name='filter_lease'),
    path('tenants', views.tenant_count, name='tenants'),
    path('lease-dates', views.filter_lease_date, name='lease_dates'),
]
