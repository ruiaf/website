from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
	return self.name

class Blog(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    category = models.ForeignKey(Category)

    def __unicode__(self):
	return self.name
