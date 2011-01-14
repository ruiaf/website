from django.shortcuts import render_to_response
from website.algorithms.models import *
from django.template import RequestContext
from string import lower

def list(request):
	algorithms = Algorithm.objects.all().order_by('name')
	c = {'algorithms': algorithms, }
	return render_to_response('algorithms/list.html', c, context_instance=RequestContext(request))

def show(request,slug):
	algorithm = Algorithm.objects.filter(slug=slug).order_by('name')[0]

	from pygments import highlight
	from pygments.lexers import get_lexer_by_name
	from pygments.formatters import HtmlFormatter

	try:
		code = open("/home/ruiaf/web/website" + algorithm.address,'r')
		lexer = get_lexer_by_name(lower(algorithm.language), stripall=True)
		formatter = HtmlFormatter(linenos=True, cssclass="highlight")
		result = highlight(code.read(), lexer, formatter)
	except:
		result = ""

	c = {'algorithm': algorithm, 'formated_code': result}
	return render_to_response('algorithms/show.html', c, context_instance=RequestContext(request))
