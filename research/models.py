from django.db import models

# Create your models here.
Countries = (
        (0, 'USA'),
        (1, 'Canada'),
        (2, 'South Korea'),
        (3, 'France'),
        (4, 'Germany'),
)

class Address(models.Model):
    title =  models.CharField(max_length=25)
    street=  models.CharField(max_length=25)
    city  =  models.CharField(max_length=25)
    state =  models.CharField(max_length=25)
    country= models.IntegerField(choices=Countries,default=0)
    zipcode= models.CharField(max_length=10)

class Person(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50,blank=True,null=True)
    address = models.ForeignKey(Address,blank=True,null=True,on_delete=models.SET_NULL)
    position = models.CharField(max_length=50,blank=True,null=True)
    affiliation = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(unique=True)
    otheremail = models.EmailField(blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    ORCID = models.CharField(blank=True,null=True,max_length=50)
    phone = models.CharField(max_length=15,null=True,blank=True)
    summary=models.TextField(null=True,blank=True)

    def __str__(self):
        """String for representing the Model object."""
        if self.middlename is None:
            return self.firstname + ' '+ self.lastname
        else:
            return self.firstname +' '+ self.middlename[0]+ '. ' + self.lastname

class Journal(models.Model):
    name =  models.CharField(max_length=50)
    acronym =  models.CharField(max_length=6)
    abrvname=  models.CharField(max_length=25)
    impactfactor = models.FloatField(blank=True,null=True)
    numreviewers = models.IntegerField(blank=True,null=True)
    summary=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

pubStatus = (
        (0,'in preparation'),
        (1,'under review'),
        (2,'published'),
)

class Article(models.Model):
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField(Person,through='AuthorOrder')
    status = models.IntegerField(choices = pubStatus,default=2)
    journal = models.ForeignKey(Journal,blank=True,null=True,on_delete=models.SET_NULL)
    volume = models.PositiveIntegerField(blank=True,null=True)
    number = models.PositiveIntegerField(blank=True,null=True)
    pages = models.PositiveIntegerField(blank=True,null=True)
    year = models.PositiveIntegerField(blank=True,null=True)
    doi = models.CharField(max_length=100,blank=True,null=True)
    url = models.URLField(blank=True,null=True)
    month = models.CharField(max_length=15,blank=True,null=True)
    abstract = models.TextField(null=True,blank=True)
    pdf = models.FileField(null=True,blank=True)
    image = models.ImageField(blank=True,null=True)

    def __str__(self):
        """String for representing the Model object."""
        if len(self.title) > 25:
            return self.title[:25] + '...'
        else:
            return self.title

class AuthorOrder(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    article= models.ForeignKey(Article, on_delete=models.CASCADE)
    order = models.IntegerField()

class Project(models.Model):
    name = models.CharField(max_length=250)
    summary = models.TextField(null=True,blank=True)
    image = models.ImageField(blank=True,null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
