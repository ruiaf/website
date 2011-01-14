from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'website.lifestream.views.lifestream'),
)
