from django.urls import path
from . import views

urlpatterns = [
    path('admins/', views.admin_list, name='admin_list'),
    path('audit-log/', views.audit_log_list, name='audit_log'),
]