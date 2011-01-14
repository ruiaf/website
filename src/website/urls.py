from django.conf.urls.defaults import *

from django.contrib import admin
from website.algorithms.models import AlgorithmSitemap
from website.sitemaps import PagesSitemap
admin.autodiscover()

sitemaps = {'flatpages': PagesSitemap,'algorithms': AlgorithmSitemap}

urlpatterns = patterns('',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
 	{'document_root': '/home/ruiaf/web/website/admin/media/'}),
    (r'^ad/(.*)', admin.site.root),
    (r'^algorithms/repo/(?P<path>.*)$', 'django.views.static.serve',
 	{'document_root': '/home/ruiaf/web/website/algorithms/repo/'}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
 	{'document_root': '/home/ruiaf/web/website/static/'}),
    (r'^rpc_relay.html$', 'django.views.static.serve',
 	{'document_root': '/home/ruiaf/web/website/static/',
		'path':'rpc_relay.html'}),
    (r'^canvas.html$', 'django.views.static.serve',
 	{'document_root': '/home/ruiaf/web/website/static/',
		'path':'canvas.html'}),
    (r'^xip/(?P<path>.*)$', 'django.views.static.serve',
 	{'document_root': '/home/ruiaf/web/website/static/xip/',
	 'show_indexes': True}),
    (r'^', include('website.blango.urls')),
    (r'^aboutme/', include('website.aboutme.urls')),
    (r'^projects/', include('website.projects.urls')),
    (r'^algorithms/', include('website.algorithms.urls')),
    (r'^timeto/', include('website.timeto.urls')),
    (r'^lifestream/', include('website.lifestream.urls')),
    (r'^basic/', include('website.basic.urls')),
)
