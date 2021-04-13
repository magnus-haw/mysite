import os 
import pickle
from django.db import models
from django.conf import settings

#Create your models here.

HOUSES = [(1,'Senate'), (2,'Assembly')]

class Agenda(models.Model):
    house = models.PositiveSmallIntegerField(choices=HOUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.last_modified)

class Hearing(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    link = models.URLField()
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.date

class Bill(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    link = models.URLField()
    hearing = models.ForeignKey(Hearing, on_delete=models.CASCADE)

    def __str__(self):
        return self.title