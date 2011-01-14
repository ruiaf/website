from django.conf.urls.defaults import *
from website.timeto.views import *

urlpatterns = patterns('',
    (r'(?P<slug>[-\w]+)/', 'website.timeto.views.show'),
    (r'', 'website.timeto.views.list'),
)
