from website.timeto.models import SpecialDay
from django.contrib import admin

class SpecialDayAdmin(admin.ModelAdmin):
	pass

admin.site.register(SpecialDay, SpecialDayAdmin)
