from django.shortcuts import render
from .models import Person, Journal, Article, Project

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    #num_books = Book.objects.all().count()
    #num_instances = BookInstance.objects.all().count()
    me = Person.objects.get(firstname='Magnus')
    address = me.address

    # Available books (status = 'a')
    #num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    #num_authors = Author.objects.count()
    
    context = {
         'me':me,
         'address':address,
    #    'num_books': num_books,
    #    'num_instances': num_instances,
    #    'num_instances_available': num_instances_available,
    #    'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'research/index.html', context=context)

def publications(request):
    articles = Article.objects.all().order_by('-year')

    context = {
            'articles':articles,
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
    context = {
            'projects':projects,
            'completedprojects':completedprojects,
    }

    # Render the HTML template other.html with the data in the context variable
    return render(request, 'research/projects.html', context=context)
