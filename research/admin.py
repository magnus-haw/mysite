from django.contrib import admin
from .models import Person, Address, AuthorOrder
from .models import Article, Journal, Project

# Register your models here.
class AuthorOrderInline(admin.TabularInline):
    model = AuthorOrder
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    list_display =('firstname','lastname','affiliation','position','email','website',)
    list_filter = ['affiliation']
    search_fields = ['firstname','lastname','email','phone','address','summary',]
    def show_phone(self, obj):
        return format_html('<a href="callto://+{url}">{url}</a>', url=obj.phone)
    def short_summary(self, obj):
        return obj.summary[0:50]

    show_phone.short_description = "Phone"
    short_summary.short_description = "Summary"
    show_phone.admin_order_field = 'phone'
    short_summary.admin_order_field = 'summary'

class AddressAdmin(admin.ModelAdmin):
    list_display = ('title', 'street','city','state','zipcode')
    list_filter = ['state']
    class Meta:
        verbose_name_plural = "addresses"

class JournalAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','journal','year','url')
    inlines = (AuthorOrderInline,)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','summary')

admin.site.register(Person,PersonAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Journal,JournalAdmin)

