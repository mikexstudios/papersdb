from django.contrib import admin

from papers import models

class CrocodocInline(admin.TabularInline):
    model = models.Crocodoc

class PaperAdmin(admin.ModelAdmin):
    list_display = ('id', 'local_id', 'user', 'title', 'authors', 'journal',
                    'year', 'is_asap', 'volume', 'issue', 'pages', 'url',
                    'file', 'hash', 'updated', 'created')
    list_display_links = ('id', 'title')

    inlines = [
        CrocodocInline,
    ]
admin.site.register(models.Paper, PaperAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'paper_increment', )
admin.site.register(models.UserProfile, UserProfileAdmin)
