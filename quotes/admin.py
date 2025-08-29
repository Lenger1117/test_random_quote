from django.contrib import admin

from .models import Source, Quote


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote', 'source', 'weight', 'likes', 'dislikes', 'views')
    list_filter = ('source', 'weight')
    search_fields = ('quote', 'source__name')
    readonly_fields = ('likes', 'dislikes', 'views')  
    empty_value_display = '-пусто-'