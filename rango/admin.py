from django.contrib import admin
from rango.models import Category, Page

# Customize how the Page is displayed in the background.
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Registration Model
admin.site.register(Category)
admin.site.register(Page, PageAdmin)
