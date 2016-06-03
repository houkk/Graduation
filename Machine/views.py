# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
import simplejson, os, shutil
import path as path
import models as md

from tree import tree as tree
from tree import createDataSet as createDataSet
from tree import treePlotter as tp
from tree import storeTree as st
from tree import classify as classify
from tree import C45 as C45

# Create your views here.
@login_required
def index(self):
    return render_to_response('index.html')

def login(self):
    return render_to_response('login.html')
@login_required
def adminIndex(self):
    return render_to_response('modules/index/admin-index.html')
@login_required
def C4dot5(self):
    return render_to_response('modules/C4dot5/C4dot5.html')

def rmdirs(routerPath):
    print routerPath
    if os.path.exists(r'%s' % routerPath):
        shutil.rmtree(routerPath)

def makedirs(tree_name):
    routerPath = path.treePath + tree_name
    rmdirs(routerPath)
    os.makedirs(routerPath + '/')
    return routerPath
    # if os.path.exists(r'')

def handle_uploaded_file(f, tree_name):
    routerPath = makedirs(tree_name)
    filePath = routerPath + '/' + f.name

    destination = open(filePath, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return routerPath, filePath

def createTree(routerPath, filePath, tree_name, classify):
    dataSet = None
    features = None
    myTree = None
    if classify == "C4.5":
        print 'C4.5 dataset'
        dataSet, features = C45.createDataSetCNDA(filePath)
        myFeatures = features[:]
        myTree = tree.createTree(dataSet, features, classify)
        C45.cutBranch_uptodown(myTree, dataSet, myFeatures)
    else:
        dataSet, features = createDataSet.createDataSet(filePath)
        myTree = tree.createTree(dataSet, features, classify)
    try:
        pngPath = tp.createPlot(myTree, routerPath, tree_name)
    except Exception as e:
        print 'e', e
        print 'e.message', e.message
    print '11pngPaht', pngPath
    treePath = st.storeTree(myTree, routerPath, tree_name)
    return pngPath, treePath

@login_required
def treeID3(request):
    f = request.FILES
    tree_name = request.POST['tree_name']
    description = request.POST['description']
    classify = request.POST['classify']
    if md.Tree.objects.filter(tree_name=tree_name):
        return HttpResponse(simplejson.dumps({'error': '数据集名称已存在，请更改!!!'}))
    rmdirs(path.treePath + tree_name)
    routerPath, filePath = '', ''
    if tree_name == '':
        return HttpResponse(simplejson.dumps({'error': '数据集名称不能为空!!!'}))
    if f == {}:
        return HttpResponse(simplejson.dumps({'error': 'Not file found Or The file has failed'}))
    try:
        routerPath, filePath = handle_uploaded_file(f['file'], tree_name)
    except Exception as e:
        print e.message
        return HttpResponse(simplejson.dumps({'error': '数据集存储失败!!!'}))
    try:
        pngPath, treePath = createTree(routerPath, filePath, tree_name, classify)
        treeSave = md.Tree(tree_name=tree_name, file_path=filePath, file_status=True, tree_path=treePath, png_path=pngPath, status=True, description=description, classify=classify)
        treeSave.save()
    except Exception as e:
        print e.message
        shutil.rmtree(routerPath)
        return HttpResponse(simplejson.dumps({'error': 'Training Failed!!!'}))

    return HttpResponse(simplejson.dumps({'success': 'Training Finished'}))

@login_required
def treeLabels(request):
    filePath = request.GET['file_path']
    result = createDataSet.createLabels(filePath)
    result.pop()
    return HttpResponse(simplejson.dumps({"labels": result}))

@login_required
def treeClassify(request):
    filePath = request.POST['file_path']
    treePath = request.POST['tree_path']
    data = request.POST.getlist('data')
    labels = createDataSet.createLabels(filePath)
    myTree = st.grabTree(treePath)
    myLabels = labels[:]
    if 'bloodpresure' in filePath:
        data[0] = C45.formatAge(data[0])
        data[2] = C45.formatBMI(data[2])
        data[3] = C45.formatSleepTime(data[2])

    result = classify.classify(myTree, myLabels, data)
    result_label = labels.pop()
    return HttpResponse(simplejson.dumps({'result': result, 'label': result_label}))
