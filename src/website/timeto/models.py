from django.db import models

class SpecialDay(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)
    date = models.DateTimeField()

    def __unicode__(self):
	return self.name
