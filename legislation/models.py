import os 
import pickle
from django.db import models
from django.conf import settings

# Create your models here.
# class AssemblyAgenda(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.last_modified

#     def update_agenda(self): 
#         path = os.path.join(settings.STATIC_ROOT, self.filename)
#         return pickle.load(open(path,'rb'))

# class AssemblyHearing(models.Model):
#     name = 
#     date = models.DateTimeField()
#     time = 
#     link = 

# class AssemblyBill(models.Model):
#     pass

# class SenateAgenda(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#     filename = models.CharField(default="senate-agenda.pk", max_length=50)

#     def __str__(self):
#         return self.filename

#     def loadfile(self): 
#         path = os.path.join(settings.STATIC_ROOT, self.filename)
#         return pickle.load(path)
    
#     def savefile(self,myobj):
#         path = os.path.join(settings.STATIC_ROOT, self.filename)
#         pickle.dump(myobj,open(path,'wb'))
#         return