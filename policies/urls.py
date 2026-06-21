from django.urls import path
from . import views

urlpatterns = [
    path('', views.policy_list, name='policy_list'),
    path('create/', views.policy_create, name='policy_create'),
    path('<int:pk>/update/', views.policy_update, name='policy_update'),
    path('<int:pk>/delete/', views.policy_delete, name='policy_delete'),
]