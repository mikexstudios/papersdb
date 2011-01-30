from django.contrib import admin

from .models import Paper

class PaperAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'authors', 'journal', 'year', 'volume', 
                    'issue', 'pages', 'url')
    list_display_links = ('id', 'title')
admin.site.register(Paper, PaperAdmin)