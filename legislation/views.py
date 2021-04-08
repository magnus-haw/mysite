from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from .utils import getFullAssemblyAgenda, getFullSenateAgenda
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
    senate = getFullSenateAgenda()
    
    context = {
         'agenda':senate,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'legislation/senate.html', context=context)

def assembly(request):
    """View function for home page of site."""

    assembly = getFullAssemblyAgenda()

    context = {
         'agenda':assembly,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'legislation/assembly.html', context=context)