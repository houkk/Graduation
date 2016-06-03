# -*- coding: utf-8 -*-

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.http import HttpResponse


def show(k, dataMat, myCentroids, clustAssing, routerPath, dataName):
    markerList = ['.', ',', '8', 'o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'D', 'd']
    fig = plt.figure()
    rect = [0.1, 0.1, 0.8, 0.8]
    # axprops = dict(xticks=[], yticks=[])
    # ax0 = fig.add_axes(rect, label='ax0', **axprops)
    # imgP = plt.imread('1.jpg')
    # ax0.imshow(imgP)
    ax1 = fig.add_axes(rect, label='ax1', frameon=False)
    # ax1 = Axes3D(fig)
    for i in range(k):
        ptsInCurrCluster = dataMat[np.nonzero(clustAssing[:, 0].A == i)[0], :]
        colors = np.random.rand(len(ptsInCurrCluster))
        markerStyle = markerList[np.random.randint(0, len(markerList)) - 1]
        # print ptsInCurrCluster[:, 2].flatten().A[0]
        ax1.scatter(
            ptsInCurrCluster[:, 0].flatten().A[0],
            ptsInCurrCluster[:, 1].flatten().A[0],
            c=colors,
            marker=markerStyle,
            s=90
        )
    ax1.scatter(
        myCentroids[:, 0].flatten().A[0],
        myCentroids[:, 1].flatten().A[0],
        c='r',
        marker='+',
        s=300

    )
    pngPath = routerPath + '/' + dataName + '.png'
    plt.show()

    # fig.savefig(pngPath)
    # plt.close(fig)
    # return pngPath
import tools
import biKmeans
def startCluster(routerPath, filePath, dataName, clusterNum):
    dataMat = np.mat(tools.loadDataSet(filePath))
    myCentroids, clustAssing = biKmeans.biKmeans(dataMat, clusterNum)
    show(clusterNum, dataMat, myCentroids, clustAssing, routerPath, dataName)

if __name__ == '__main__':
    routerPath = '/'
    dataName = 'test'
    clusterNum = 4
    filePath = 'sport.txt'
    startCluster(routerPath, filePath, dataName, clusterNum)