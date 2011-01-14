from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'(?P<slug>[-\w]+)/', 'website.algorithms.views.show'),
    (r'', 'website.algorithms.views.list'),
)
