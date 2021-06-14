import os 
import pickle
from django.db import models
from django.conf import settings

#Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Person(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "People"

class Team(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    people = models.ManyToManyField(Person)

    def __str__(self):
        return self.name

class Session(BaseModel):
    HOUSES = [('Senate','Senate'), ('Assembly','Assembly')]
    state = models.CharField(max_length=100, default='CA')
    house = models.CharField(max_length=100, choices=HOUSES, default='Assembly')
    year_start = models.PositiveIntegerField()
    year_end = models.PositiveIntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.state+ " ")+str(self.house)+str(self.year_start)

class Sector(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null = True, blank=True)

    def __str__(self):
        return self.name

class Bill(BaseModel):
    STANCES = [(1,'Support'), (2,'Oppose'), (3,'Ignore')]
    EFFORT = [(1,'Low'), (2,'Medium'), (3, 'High')]

    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField(null=True, blank=True)
    author = models.CharField(max_length=50, null=True, blank=True)
    link = models.URLField(null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True, blank=True,)
    strategy = models.CharField(max_length=200, null=True, blank=True,)
    comments = models.TextField(null=True, blank=True)

    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    mitigation = models.BooleanField(null = True, blank=True)
    adaptation = models.BooleanField(null = True, blank=True)
    stance = models.PositiveSmallIntegerField(null=True, blank=True, choices=STANCES)
    effort = models.PositiveSmallIntegerField(null=True, blank=True, choices=EFFORT)

    def __str__(self):
        return self.name

class BillAmendment(BaseModel):
    IMPORTANCE = [(1,'Low'), (2,'Medium'), (3, 'High')]
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    importance = models.PositiveSmallIntegerField(null=True, blank=True, choices=IMPORTANCE)

    def __str__(self):
        return str(self.bill.name + " ")+str(self.last_modified)

class FileAttachment(BaseModel):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    file = models.FileField()

    def __str__(self):
        return self.name

class Committee(BaseModel):
    name = models.CharField(max_length=100)
    link = models.URLField()
    description = models.CharField(max_length=200, null=True, blank=True)
    responsible_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Hearing(BaseModel):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    date = models.DateField()
    letter_due_date = models.DateField(null=True)
    letter_date_confirmed = models.BooleanField(default=False)
    time = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    link = models.URLField()
    bills = models.ManyToManyField(Bill)

    def __str__(self):
        return self.committee.name + " " + str(self.date)

class SupportLetter(BaseModel):
    STATUS = [(1,'Unassigned'), (2,'Assigned'), (3, 'Sent')]
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    hearing = models.ForeignKey(Hearing, on_delete=models.CASCADE)
    letter_due_date = models.DateField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(default=1,choices=STATUS)
    volunteers = models.ManyToManyField(Person, blank=True)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return str(self.bill.name + " ") + str(self.hearing.date)
