# -*- coding: utf-8 -*-
import serializers as sl
import filter as fl
import models as md
from rest_framework import viewsets
from django.db.models import Q

class TreeViewSet(viewsets.ModelViewSet):

    queryset = md.Tree.objects.all()
    serializer_class = sl.TreeSerializer
    filter_class = fl.TreeFilter

class TwoKViewSet(viewsets.ModelViewSet):

    queryset = md.towK.objects.all()
    serializer_class = sl.TwoKSerializer
    filter_class = fl.TwoKFilter
