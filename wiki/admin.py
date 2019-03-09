from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Category,Topic,Subtopic,Article

# Register your models here.

class ArticleInline(GenericTabularInline):
    model = Article
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','created','visible',)
    inlines = (ArticleInline,)
    readonly_fields= ['updated', 'created',]

class TopicAdmin(admin.ModelAdmin):
    list_display=('name','created','visible',)
    inlines = (ArticleInline,)
    readonly_fields= ['updated', 'created',]

class SubtopicAdmin(admin.ModelAdmin):
    list_display=('name','created','visible',)
    inlines = (ArticleInline,)
    readonly_fields= ['updated', 'created',]

class ArticleAdmin(admin.ModelAdmin):
    list_display=('name','created','visible',)
    readonly_fields= ['updated', 'created','object_id',
                      'content_object','content_type']

admin.site.register(Subtopic,SubtopicAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Category,CategoryAdmin)
