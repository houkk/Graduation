# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from Machine import models as md
from Machine import path as path
from Machine.views import rmdirs

import simplejson, os, shutil, sys
import tools as tools
import biKmeans as biKmeans
import numpy as np
from matplot import show

@login_required
def towK(self):
    return render_to_response('modules/towK/two_k.html')

def makedirs(dataName):
    routerPath = path.kPath + dataName
    rmdirs(routerPath)
    os.makedirs(routerPath + '/')
    return routerPath


def handle_uploaded_file(f, dataName):
    routerPath = makedirs(dataName)
    filePath = routerPath + '/' + f.name

    destination = open(filePath, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return routerPath, filePath


def startCluster(routerPath, filePath, dataName, clusterNum):
    dataMat = np.mat(tools.loadDataSet(filePath))
    myCentroids, clustAssing = biKmeans.biKmeans(dataMat, clusterNum)
    pngPath = show(clusterNum, dataMat, myCentroids, clustAssing, routerPath, dataName)

    return pngPath

@login_required
def k_view(request):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    f = request.FILES
    dataName = request.POST['dataName']
    description = request.POST['description']
    clusterNum = int(request.POST['clusterNum'])
    if dataName == '':
        return HttpResponse(simplejson.dumps({'error': '数据集名称不能为空!!!'}))

    if md.towK.objects.filter(dataName=dataName):
        return HttpResponse(simplejson.dumps({'error': '数据集名称已存在，请更改!!!'}))
    rmdirs(path.kPath + dataName)

    routerPath, filePath = '', ''

    if f == {}:
        return HttpResponse(simplejson.dumps({'error': 'Not file found Or The file has failed'}))

    try:
        routerPath, filePath = handle_uploaded_file(f['file'], dataName)
    except Exception as e:
        print e.message
        return HttpResponse(simplejson.dumps({'error': '数据集存储失败!!!'}))

    try:
        pngPath = startCluster(routerPath, filePath, dataName, clusterNum)
        treeSave = md.towK(dataName=dataName, clusterNum=clusterNum, pngPath=pngPath, file_path=filePath, description=description)
        treeSave.save()
    except Exception as e:
        print '---------------------------------'
        print e.message
        shutil.rmtree(routerPath)
        return HttpResponse(simplejson.dumps({'error': 'Clustering Failed!!!'}))

    return HttpResponse(simplejson.dumps({'success': 'Clustering Succeed'}))