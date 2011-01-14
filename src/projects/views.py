from django.shortcuts import render_to_response

def show(request):
	c = {	'items': None, }
	return render_to_response('projects/projects.html', c)

