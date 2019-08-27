from django.shortcuts import render
from .models import Person, Journal, Article, Project, Page

# Create your views here.
def index(request):
    """View function for home page of site."""

    page = Page.objects.get(name='home')
    me = page.person
    address = me.address
    last_mod = page.last_modified

    context = {
         'page':page,
         'me':me,
         'address':address,
         'last_mod':last_mod,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'research/index.html', context=context)

def publications(request):
    others = Article.objects.filter(peerreviewed = False).order_by('-year')
    articles = Article.objects.filter(peerreviewed = True).order_by('-year')
    last = Article.objects.latest()
    context = {
            'articles':articles,
            'others':others,
            'last_mod':last.last_modified,
    }

    # Render the HTML template publications.html with the data in the context variable
    return render(request, 'research/publications.html', context=context)

def other(request):

    context = {

    }

    # Render the HTML template other.html with the data in the context variable
    return render(request, 'research/other.html', context=context)

def projects(request):
    completedprojects = Project.objects.filter(completed = True)
    projects = Project.objects.filter(completed = False)
    last = Project.objects.latest()

    context = {
            'projects':projects,
            'completedprojects':completedprojects,
            'last_mod':last.last_modified,
    }

    # Render the HTML template other.html with the data in the context variable
    return render(request, 'research/projects.html', context=context)
