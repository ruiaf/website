from django.shortcuts import render_to_response
from website.timeto.models import *
from string import lower

def list(request):
	specialdays = SpecialDay.objects.all().order_by('date')
	c = {'specialdays': specialdays, }
	return render_to_response('timeto/list.html', c)

def show(request,slug):
	specialday = SpecialDay.objects.filter(slug=slug).order_by('name')[0]
	c = {'specialday': specialday}
	return render_to_response('timeto/show.html', c)
