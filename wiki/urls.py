from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='wiki'),
    path('category/<int:pk>', views.category_detail, name='category_detail'),
    path('topic/<int:pk>', views.topic_detail, name='topic_detail'),
    path('subtopic/<int:pk>', views.subtopic_detail, name='subtopic_detail'),
    path('article/<int:pk>', views.article_detail, name='article_detail'),
]
