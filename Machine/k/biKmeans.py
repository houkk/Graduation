# -*- coding: utf-8 -*-

import tools as tools
import kMeans as kMeans
from matplot import show
import numpy as np

def biKmeans(dataSet, k):
    m = np.shape(dataSet)[0] # row
    # print dataSet
    clusterAssment = np.mat(np.zeros((m, 2)))
    centroid0 = np.mean(dataSet, axis=0).tolist()[0]
    centList = [centroid0]
    for j in range(m):
        clusterAssment[:, 1] = tools.distEclud(np.mat(centroid0), dataSet[j, :]) ** 2
    count = 0
    while len(centList) < k:
        lowestSSE = np.inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[np.nonzero(clusterAssment[:, 0].A == i)[0], :]
            # 质心对应的数据集
            centroidMat, splitClustAss = kMeans.kMeans(ptsInCurrCluster, 2)
            sseSplit = np.sum(splitClustAss[:, 1])
            # 划分后的SSE
            sseNotSplit = np.sum(clusterAssment[np.nonzero(clusterAssment[:, 0].A != i)[0], 1])
            # 未划分的SSE
            # print "sseSplit, and notSplit: ", sseSplit, sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit

        bestClustAss[np.nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)
        bestClustAss[np.nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        # print 'the bestCentToSplit is: ', bestCentToSplit
        # print 'the len of bestClustAss is: ', len(bestClustAss)
        centList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]
        centList.append(bestNewCents[1, :].tolist()[0])
        clusterAssment[np.nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0], :] = bestClustAss
    return np.mat(centList), clusterAssment

def main():
    dataMat = tools.loadDataSet('/home/mesogene/PycharmProjects/GraduationProject/templates/k/test1/testSet.txt')
    print dataMat
    dataMat = np.mat(dataMat)
    k = 3
    # print dataMat
    myCentroids, clustAssing = biKmeans(dataMat, 4)

    # show(k, dataMat, myCentroids, clustAssing)
    print myCentroids# , clustAssing

if __name__ == '__main__':
    main()