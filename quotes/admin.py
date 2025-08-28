from django.contrib import admin

from quotes.models import Quote, Category, Source


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    fields = ('text', 'source', 'weight', 'views', 'user')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    fields = ('name', 'category', 'user')
