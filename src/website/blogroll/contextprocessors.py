from website.blogroll.models import *

def blogroll(request):

    categories = Category.objects.all().order_by('name')
    blogs={}

    for category in categories:
	blogs[category.name]=Blog.objects.filter(category=category).order_by('name')

    return {'blogs': blogs}
