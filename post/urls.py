from django.urls import path, re_path
from . import views
urlpatterns = [
    path('put', views.put),
    re_path('(\d+)', views.get),
    path('', views.getall),
]
