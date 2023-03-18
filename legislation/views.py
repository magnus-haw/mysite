from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from .utils import getFullAssemblyAgenda, getFullSenateAgenda, saveAgenda
from .models import Session, Bill

# Create your views here.

def index(request):
    """View function for home page of site."""
    
    context = {
         'page':0,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'legislation/index.html', context=context)

def bill_list(request):
    """View function for home page of site."""
    now = timezone.now()
    ss = Session.objects.filter(year_start=now.year)
    bills = Bill.objects.filter(session__in=ss)
    context = {
         'bills':bills,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'legislation/bill_list.html', context=context)

def senate(request):
    """View function for home page of site."""
    #senate = getFullSenateAgenda()
    search = Session.objects.filter(house='Senate')
    print(search)
    if len(search) > 0:
        agenda = search.latest('created_at')
    else:
        sorted_agendas = getFullSenateAgenda()
        saveAgenda(sorted_agendas, 'Senate')
        agenda = Session.objects.filter(house='Senate').latest('created_at')
    hearings = agenda.hearing_set.filter(date__gte=timezone.now() )
    context = {
         'agenda':agenda,
         'hearings':hearings,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'legislation/senate.html', context=context)

def assembly(request):
    """View function for home page of site."""
    #assembly = getFullAssemblyAgenda()
    search = Session.objects.filter(house='Assembly')
    if len(search) > 0:
        agenda = search.latest('created_at')
    else:
        sorted_agendas = getFullAssemblyAgenda()
        saveAgenda(sorted_agendas, 'Assembly')
        agenda = Session.objects.filter(house='Assembly').latest('created_at')
    hearings = agenda.hearing_set.filter(date__gte=timezone.now() )    
    context = {
         'agenda':agenda,
         'hearings':hearings,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'legislation/assembly.html', context=context)
