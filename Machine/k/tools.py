# -*- coding: utf-8 -*-
import numpy as np

def loadDataSet(fileName):
    print fileName
    # 将文本文件导入列表，并且转换为float
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        fitLine = map(float, curLine)
        dataMat.append(fitLine)
    return dataMat

def distEclud(vecA, vecB):
    # 欧氏距离
    return np.sqrt(np.sum(np.power(vecA - vecB, 2)))

def randCent(dataSet, k):
    # 构建包含k个随机质心的集合
    n = np.shape(dataSet)[1]
    # col

    centroids = np.mat(np.zeros((k, n)))
    for j in range(n):
        minJ = np.min(dataSet[:, j])
        rangeJ = float(np.max(dataSet[:, j]) - minJ)
        centroids[:, j] = minJ + rangeJ * np.random.rand(k, 1)
    return centroids

def main():
    filePath = 'testSet.txt'
    dataMat = np.mat(loadDataSet(filePath))
    print np.min(dataMat[:, 0])
    print np.max(dataMat[:, 0])
    print np.min(dataMat[:, 1])
    print np.max(dataMat[:, 1])
    print randCent(dataMat, 2)

if __name__ == '__main__':
    main()