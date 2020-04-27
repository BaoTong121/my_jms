from django.urls import path, include
from . import views
urlpatterns = [
    path('reg/', views.reg),
    path('login/', views.login),
    path('test/', views.test),
]
