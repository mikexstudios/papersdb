from django.contrib import admin

from .models import Paper, Import

class PaperAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'authors', 'journal', 'year', 'volume', 
                    'issue', 'pages', 'url', 'file', 'hash',)
    list_display_links = ('id', 'title')
admin.site.register(Paper, PaperAdmin)

class ImportAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_done', 'data',)
    list_display_links = ('id', )
admin.site.register(Import, ImportAdmin)
