from django.contrib import admin
from .models import Connection, Archive, Tag

# Does not need a modeladmin
admin.site.register(Tag)

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'executive_board', 'ima_board',)
    list_filter = ('executive_board', 'ima_board')
    search_fields = ('name', 'email')
    ordering = ('name',)

admin.site.register(Connection, ConnectionAdmin)

class ArchiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    list_filter = ('tag',)
    search_fields = ('name', 'title')
    ordering = ('name',)

admin.site.register(Archive, ArchiveAdmin)