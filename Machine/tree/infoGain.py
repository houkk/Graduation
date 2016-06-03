# -*- coding: utf-8 -*-
# 决策树
# ID3 划分数据集

from math import log

def createDataSet():
    dataSet = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

def calcShannonEnt(dataSet):
    # 计算香农熵
    numEntries = len(dataSet)
    labelCount = {}
    for featVec in dataSet:
        # 最后一列是目标变量，即分类
        currentLabel = featVec[-1]
        if currentLabel not in labelCount.keys():
            # 将所有可能分类加入字典
            labelCount[currentLabel] = 0
        labelCount[currentLabel] += 1
    shannonEat = 0.0
    for key in labelCount:
        prob = float(labelCount[key]) / numEntries
        # 概率

        shannonEat -= prob * log(prob if prob > 0 else 1, 2)
    return shannonEat

def splitDataSet(dataSet, axis, value):
    # 根据特征值 划分数集
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reduceFeatVec = featVec[:axis]
            reduceFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet

def choseBestFeatureToSplit(dataSet):
    # 计算split（每种特征值）数据集的香农熵和dataSet基本数据集比较，取出最大信息增益（baseEntropy-newEntropy）
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1

    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)# 去重
        newEntropy = 0.0

        # 每种划分方式（特征值）的香农熵
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy

        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i

    return bestFeature
