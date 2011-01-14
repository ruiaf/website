from django.shortcuts import render_to_response
from django.template import RequestContext

def show(request):
	c = {	'items': None, }
	return render_to_response('aboutme/aboutme.html', c, context_instance=RequestContext(request))

