# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import simplejson

import models as md
import views
import path as path

@login_required
def cleanTree(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        tree = md.Tree.objects.filter(tree_id=id)
        treeName = tree[0].tree_name
        views.rmdirs(path.treePath + treeName)
    return HttpResponse(simplejson.dumps({"success": "clean"}))

@login_required
def cleanK(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        towk = md.towK.objects.filter(kid=id)
        filename = towk[0].dataName
        views.rmdirs(path.kPath + filename)
    return HttpResponse(simplejson.dumps({"success": "clean"}))
