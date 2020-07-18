from django.urls import path
from . import views


urlpatterns = [
    path('', views.register_view, name='register_view'),
    path('verify/', views.verify, name='verify'),
    # path('login/', views.mobile_login, name='mobile_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
