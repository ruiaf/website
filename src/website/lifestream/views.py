from django.shortcuts import render_to_response
from django.template import RequestContext
from string import strip

import friendfeed

def lifestream(request,istart=0,inum=90):
	service = friendfeed.FriendFeed()
	searchstring=None
	xhr = request.POST.has_key('xhr')
	itemlist = []
	try:
		searchstring=request.POST['search']
		if strip(searchstring)=='':
			searchstring=''
			raise Exception
		feed = service.search("who:ruiaf %s"%(searchstring))
		itemlist.extend(feed['entries'])
	except:
		for i in range(0,inum,30):
			feed = service.fetch_user_feed('ruiaf',start=i,num=i+30)
			itemlist.extend(feed['entries'])
		
	c = {'items': itemlist, 'search':searchstring}
	if xhr:
		return render_to_response('django-friendfeed/django-friendfeed-content.html', c, context_instance=RequestContext(request))
	return render_to_response('django-friendfeed/django-friendfeed.html', c, context_instance=RequestContext(request))

