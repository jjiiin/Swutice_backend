from django.urls import path
from . import views
from . import scrap_no1
urlpatterns = [
    path('', views.scrap, name='scrap'),
]