# -*- coding: utf-8 -*-

import numpy as np
import tools as tools
import matplotlib
import matplotlib.pyplot as plt
from matplot import show

def kMeans(dataSet, k):
    m = np.shape(dataSet)[0]
    # row

    clusterAssment = np.mat(np.zeros((m, 2)))
    centroids = tools.randCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = np.inf
            # inf 无穷大
            minIndex = -1

            for j in range(k):
                distJI = tools.distEclud(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2
        # print centroids
        for cent in range(k):
            ptsInClust = dataSet[np.nonzero(clusterAssment[:, 0].A == cent)[0]]
            # 取出dataSet中同一质点cent的集合

            centroids[cent, :] = np.mean(ptsInClust, axis=0)
            # dataSet中同一质点对应数据集，每列求平均值，映射到质心集合中

    return centroids, clusterAssment

def main(self):
    k = 4
    dataMat = np.mat(tools.loadDataSet('./Machine/k/testSet.txt'))
    myCentroids, clustAssing = kMeans(dataMat, k)
    response = show(k, dataMat, myCentroids, clustAssing)
    print myCentroids#, clustAssing
    return response

if __name__ == '__main__':
    main()