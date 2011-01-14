from website.blogroll.models import *
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name']

class BlogAdmin(admin.ModelAdmin):
	list_display = ['name','category']
	list_filter = ['category']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
