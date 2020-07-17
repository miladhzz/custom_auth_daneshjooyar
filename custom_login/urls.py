from django.urls import path
from . import views


urlpatterns = [
    path('', views.mobile_login, name='mobile_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
