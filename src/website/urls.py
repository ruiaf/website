from django.conf.urls.defaults import *

from django.contrib import admin
from website.algorithms.models import AlgorithmSitemap
from website.sitemaps import PagesSitemap
admin.autodiscover()

sitemaps = {'flatpages': PagesSitemap,'algorithms': AlgorithmSitemap}

urlpatterns = patterns('',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    (r'^ad/(.*)', admin.site.root),
    (r'^', include('website.blango.urls')),
    (r'^aboutme/', include('website.aboutme.urls')),
    (r'^projects/', include('website.projects.urls')),
    (r'^algorithms/', include('website.algorithms.urls')),
    (r'^timeto/', include('website.timeto.urls')),
    (r'^lifestream/', include('website.lifestream.urls')),
    (r'^basic/', include('website.basic.urls')),
)
