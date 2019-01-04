from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('publications/', views.publications, name='publications'),
    path('other/', views.other, name='other'),
    path('projects/', views.projects, name='projects'),
]
