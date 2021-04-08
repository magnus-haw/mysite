from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='legislation'),
    path('senate/', views.senate, name='senate'),
    path('assembly/', views.assembly, name='assembly'),
]
