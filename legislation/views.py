from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from .utils import getFullAssemblyAgenda, getFullSenateAgenda, saveAgenda
from .models import Agenda

# Create your views here.

def index(request):
    """View function for home page of site."""
    
    context = {
         'page':0,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'legislation/index.html', context=context)

def senate(request):
    """View function for home page of site."""
    #senate = getFullSenateAgenda()
    search = Agenda.objects.filter(house=1)
    print(search)
    if len(search) > 0:
        agenda = search.latest('created_at')
    else:
        sorted_agendas = getFullSenateAgenda()
        saveAgenda(sorted_agendas, 1)
        agenda = Agenda.objects.filter(house=1).latest('created_at')

    context = {
         'agenda':agenda,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'legislation/senate.html', context=context)

def assembly(request):
    """View function for home page of site."""
    #assembly = getFullAssemblyAgenda()
    search = Agenda.objects.filter(house=2)
    if len(search) > 0:
        agenda = search.latest('created_at')
    else:
        sorted_agendas = getFullAssemblyAgenda()
        saveAgenda(sorted_agendas, 2)
        agenda = Agenda.objects.filter(house=2).latest('created_at')
    
    context = {
         'agenda':agenda,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'legislation/assembly.html', context=context)