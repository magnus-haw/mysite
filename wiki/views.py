from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from .models import Article,Subtopic,Topic,Category,HtmlBlock

# Create your views here.
def index(request):
    categories = Category.objects.filter(visible=True)
    latest = Article.objects.all().order_by('-updated')[:5]
    htmlblock = get_object_or_404(HtmlBlock,name="wiki_index")
    return render(request, 'wiki/index.html',{'categories':categories,'latest':latest,'htmlblock':htmlblock})

@login_required
def category_detail(request,pk):
    categories = Category.objects.filter(visible=True)
    category = get_object_or_404(Category,pk=pk)
    context = {'categories':categories,'category':category}
    return render(request,'wiki/category_detail.html',context)

@login_required
def topic_detail(request,pk):
    categories = Category.objects.filter(visible=True)
    topic = get_object_or_404(Topic,pk=pk)
    context = {'categories':categories,'topic':topic}
    return render(request,'wiki/topic_detail.html',context)

@login_required
def subtopic_detail(request,pk):
    categories = Category.objects.filter(visible=True)
    subtopic = get_object_or_404(Subtopic,pk=pk)
    context = {'categories':categories,'subtopic':subtopic}
    return render(request,'wiki/subtopic_detail.html',context)

@login_required
def article_detail(request,pk):
    categories = Category.objects.filter(visible=True)
    article = get_object_or_404(Article,pk=pk)
    context = {'categories':categories,'article':article}
    return render(request,'wiki/article_detail.html',context)
