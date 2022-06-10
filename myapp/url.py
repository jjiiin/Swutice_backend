from django.urls import include, re_path
from . import views
urlpatterns = [
    re_path('', views.scrap, name='scrap'),
    re_path('',views.job, name="job"),
]