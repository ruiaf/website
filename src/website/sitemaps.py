from django.contrib.sitemaps import Sitemap
from datetime import *

pages=[{'location':'/','lastmod':datetime.today()},
       {'location':'/aboutme/','lastmod':datetime(2008,11,04)},
       {'location':'/algorithms/','lastmod':datetime.today()},
	]

class PagesSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.5

	def items(self):
		return pages

	def lastmod(self, obj):
		return obj['lastmod']

	def location(self, obj):
		return obj['location']
