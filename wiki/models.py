from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType

from research.models import Person

# Create your models here.

class Article(models.Model):
    name = models.CharField(max_length=100)
    text = RichTextField(config_name='minutes')
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now= True)
    author = models.ForeignKey(Person,null=True,on_delete=models.SET_NULL)
    visible = models.BooleanField(default=True)

    content_type =   models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    text = RichTextField(config_name='minutes')
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now= True)
    visible = models.BooleanField(default=True)
    articles = GenericRelation(Article)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class Topic(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    text = RichTextField(config_name='minutes')
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now= True)
    visible = models.BooleanField(default=True)
    articles = GenericRelation(Article)
    
    def __str__(self):
        return self.name

class Subtopic(models.Model):
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = RichTextField(config_name='minutes')
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now= True)
    visible = models.BooleanField(default=True)
    articles = GenericRelation(Article)
    
    def __str__(self):
        return self.name




