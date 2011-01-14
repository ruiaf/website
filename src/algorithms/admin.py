from website.algorithms.models import Algorithm
from django.contrib import admin

class AlgorithmAdmin(admin.ModelAdmin):
	list_filter = ['language']
	list_display = ['name', 'language','description']
	search_fields = ['name', 'language','description']


admin.site.register(Algorithm, AlgorithmAdmin)
