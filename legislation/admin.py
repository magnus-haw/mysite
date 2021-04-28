from django.contrib import admin
from .models import Person, Team, Session, Sector, Bill
from .models import BillAmendment, FileAttachment, Committee
from .models import SupportLetter, Hearing

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display =('name','email', 'last_modified')
    search_fields = ['name','email',]

class TeamAdmin(admin.ModelAdmin):
    list_display =('name','description', 'last_modified')
    search_fields = ['name','description','people',]

class SessionAdmin(admin.ModelAdmin):
    list_display =('state','house','year_start','description', 'last_modified')
    search_fields = ['state','house','year_start','description',]

class SectorAdmin(admin.ModelAdmin):
    list_display =('name','description', 'team', 'last_modified')
    search_fields = ['name','description','team',]

class BillAmendmentInline(admin.TabularInline):
    model = BillAmendment
    extra = 0

class FileAttachmentInline(admin.TabularInline):
    model = FileAttachment
    extra = 0

class SupportLetterInline(admin.TabularInline):
    model = SupportLetter
    extra = 0

class BillAdmin(admin.ModelAdmin):
    list_display =('name','author','sector','mitigation','adaptation', 'stance','effort','description', 'last_modified')
    search_fields = ['name','author','description', 'sector','mitigation','adaptation', 'stance','effort','strategy', 'comments']
    list_filter = ['sector','stance','last_modified']
    inlines = (BillAmendmentInline,SupportLetterInline,FileAttachmentInline,)

class CommitteeAdmin(admin.ModelAdmin):
    list_display =('name','link','description','last_modified')
    search_fields = ['name','link','description','last_modified',]

class HearingAdmin(admin.ModelAdmin):
    list_display = ('committee','session','date','time','letter_due_date','last_modified')
    list_filter = ['letter_due_date','last_modified',]
    search_fields = ['committee','session','date','time','letter_due_date','bills']

class BillAmendmentAdmin(admin.ModelAdmin):
    list_display = ('bill','date','description','importance','last_modified')
    list_filter = ['importance','last_modified',]
    search_fields = ['bill','date','description','importance','last_modified']

admin.site.register(BillAmendment, BillAmendmentAdmin)
admin.site.register(Hearing, HearingAdmin)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Team, TeamAdmin)