#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# original based on sci-kit hashing function
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from io import StringIO

import os, string, pickle, random, uuid, urllib

def id_generator(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def get_upload_path():

	while True:
		filename = "%s.%s" % (id_generator(), "model")

		file_url = "%s%s" % (settings.MEDIA_URL, filename)

		if settings.DEBUG or urllib.urlopen(file_url).getcode() != 200:
			break

	return settings.USER_ESTIMATOR_PATH + filename

def get_upload_path_instance(instance, filename):
	if instance.object_file:

		filename = instance.object_file.name

		if settings.DEBUG:
			instance.object_file.delete(save=True)

		return filename

	else:
		return get_upload_path()



class Estimator(models.Model):

	"""This class creates estimator objects that persists predictive models

		An Estimator instance has multiple attributes

			:description:
			:estimator:

			>>> from estimators.models import Estimator
			>>> est = Estimator()
			>>> est.estimator = object
			>>> est.description = "k-means with 5 clusters"
			>>> est.save()

	"""

	creation_date = models.DateTimeField(auto_now_add=True, blank=False, null=False, editable=False)
	last_modified_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
	object_file = models.FileField(upload_to=get_upload_path_instance, default="", blank=True, editable=False)
	description = models.CharField(max_length=256)

	def __repr__(self):
		return '<Estimator <Id %s>: %s>' % (self.id, self.estimator)

	@property
	def estimator(self):
		"""return the estimator, and load it into memory if it hasn't been loaded yet"""
		return self.get_object()

	@estimator.setter
	def estimator(self, obj):
		self.set_object(obj)

	def get_object(self):
		if settings.DEBUG:
			return pickle.load(self.object_file)
		else:
			object_url = "%s%s" % (settings.MEDIA_URL, self.object_file)
			model = urllib.urlopen(object_url).read()
			return pickle.loads(model)

	def set_object(self, object_file):
		old_name = self.object_file.name # Not used for now

		buf = StringIO(pickle.dumps(object_file))  # `data` is your stream of bytes
		buf.seek(0, 2)  # Seek to the end of the stream, so we can get its length with `buf.tell()`
		temp_filename = str(uuid.uuid4())
		file = InMemoryUploadedFile(buf, "Scikit Model", temp_filename, "application/octet-stream", buf.tell(), None)
		self.object_file.save(file.name, file)  # `object_file` is an instance of `Estimator`
		self.save()

	def save(self, *args, **kwargs):
		self.last_modified_date = timezone.now()
		super(Estimator, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.object_file.delete(save=True)
		super(Estimator, self).delete(*args, **kwargs)
