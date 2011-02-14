from django.contrib import admin

from .models import Paper, UserProfile

class PaperAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'authors', 'journal', 'year', 'volume', 
                    'issue', 'pages', 'url', 'file', 'hash',)
    list_display_links = ('id', 'title')
admin.site.register(Paper, PaperAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'paper_increment', )
admin.site.register(UserProfile, UserProfileAdmin)
