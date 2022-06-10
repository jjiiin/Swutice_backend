from django.urls import include, re_path
from . import views
from . import task

urlpatterns = [
    re_path('', views.scrap, name='scrap'),   
]