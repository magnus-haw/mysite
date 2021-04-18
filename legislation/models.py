import os 
import pickle
from django.db import models
from django.conf import settings

#Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Person(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Team(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    people = models.ManyToManyField(Person)

class Session(BaseModel):
    HOUSES = [(1,'Senate'), (2,'Assembly')]
    house = models.PositiveSmallIntegerField(choices=HOUSES)
    year_start = models.PositiveIntegerField()
    year_end = models.PositiveIntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.last_modified)

class Sector(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null = True, blank=True)

class Bill(models.Model):
    STANCES = [(1,'Support'), (2,'Oppose'), (3,'Ignore')]
    EFFORT = [(1,'Low'), (2,'Medium'), (3, 'High')]

    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    link = models.URLField()
    description = models.CharField(max_length=200, null=True, blank=True,)
    strategy = models.CharField(max_length=200, null=True, blank=True,)
    comments = models.TextField(null=True, blank=True,)

    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    mitigation = models.BooleanField(null = True, blank=True)
    adaptation = models.BooleanField(null = True, blank=True)
    stance = models.PositiveSmallIntegerField(null=True, blank=True, choices=STANCES)
    effort = models.PositiveSmallIntegerField(null=True, blank=True, choices=EFFORT)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BillAmendment(BaseModel):
    IMPORTANCE = [(1,'Low'), (2,'Medium'), (3, 'High')]
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    importance = models.PositiveSmallIntegerField(null=True, blank=True, choices=IMPORTANCE)

class FileAttachment(BaseModel):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    file = models.FileField()

class Committee(BaseModel):
    name = models.CharField(max_length=100)
    link = models.URLField()
    description = models.CharField(max_length=200)

class Hearing(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    date = models.DateField()
    letter_due_date = models.DateField()
    time = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    link = models.URLField()
    bills = models.ManyToManyField(Bill)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.committee.name + " " + self.date

class SupportLetter(BaseModel):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    hearing = models.ForeignKey(Hearing, on_delete=models.CASCADE)
    letter_due_date = models.DateField()
    volunteers = models.ManyToManyField(Person)


