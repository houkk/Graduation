from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Tree(models.Model):
    tree_id = models.AutoField(primary_key=True)
    tree_name = models.CharField(max_length=20, unique=True)
    file_path = models.CharField(max_length=100, blank=True, null=True)
    file_status = models.BooleanField(default=False)
    tree_path = models.CharField(max_length=100, blank=True, null=True)
    png_path = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, blank=True, null=True)
    classify = models.CharField(max_length=10, blank=True, null=True)


class towK(models.Model):
    kid = models.AutoField(primary_key=True)
    dataName = models.CharField(max_length=20, unique=True)
    clusterNum = models.IntegerField(null=False, blank=False)
    pngPath = models.CharField(max_length=100, blank=True, null=True)
    file_path = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
