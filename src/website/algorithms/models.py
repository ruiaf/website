from django.db import models
from django.contrib.sitemaps import Sitemap

class Algorithm(models.Model):
	slug = models.SlugField(max_length=30)
	name = models.CharField(max_length=30)
	language = models.CharField(max_length=30)
	description = models.TextField(max_length=500)
	address = models.CharField(max_length=50)
	pub_date = models.DateTimeField()
	
	def __unicode__(self):
        	return "%s in %s"%(self.name,self.language)

class AlgorithmSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.5

	def items(self):
		return Algorithm.objects.all()

	def lastmod(self, obj):
		return obj.pub_date

	def location(self, obj):
		return "/algorithms/%s/"%(obj.slug)
