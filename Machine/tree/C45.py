# -*- coding: utf-8 -*-
import xlrd
import xlwt
import math, os, sys
import operator
from datetime import date, datetime
from sklearn import datasets
import infoGain as ig
import tree as tree
import treePlotter as tp
from matplotlib import pyplot as plt

def formatAge(age):
    result = None
    age = int(age)
    if age in range(1, 21):
        result = '1-20'
    if age in range(21, 41):
        result = '21-40'
    if age in range(41, 61):
        result = '41-60'
    if age in range(61, 81):
        result = '61-80'
    if age in range(81, 101):
        result = '81-100'
    return result

def formatBMI(BMI):
    result = None
    if BMI < 18.5:
        result = 'Low'
    if 25 > BMI >= 18.5:
        result = 'Normal'
    if 25 <= BMI < 28:
        result = 'Overweight'
    if 28 <= BMI <= 32:
        result = 'fat'
    if BMI >= 32:
        result = 'VeryFat'
    return result

def formatSleepTime(time):
    result = None
    if time < 7:
        result = 'short'
    if 7 <= time <= 10:
        result = 'normal'
    if 10 < time:
        result = 'long'
    return result


def createDataSetCNDA(filePath):
    data = xlrd.open_workbook(filePath)
    from_sheet = data.sheet_by_index(0)
    # 通过索引获取sheet
    id_array = from_sheet.row_values(0)
    # 获取某行数据
    ncols_length = from_sheet.ncols
    # 获取列数
    nrows_length = from_sheet.nrows
    # 获取行数
    features = id_array
    # print features
    dataSet = [[] for i in range(0, (nrows_length - 1))]
    for var1 in range(1, nrows_length):
        temp = from_sheet.row_values(var1)
        for var2 in range(ncols_length):
            if var2 == 0:
                temp[var2] = formatAge(temp[var2])
            if var2 == 2:
                temp[var2] = formatBMI(temp[var2])
            if var2 == 3:
                temp[var2] = formatSleepTime(temp[var2])
            dataSet[var1 - 1].append(temp[var2])
    return dataSet, features

def createDataSetxls(filePath):
    data = xlrd.open_workbook(filePath)
    from_sheet = data.sheet_by_index(0)
    # 通过索引获取sheet
    id_array = from_sheet.row_values(0)
    # 获取某行数据
    ncols_length = from_sheet.ncols
    # 获取列数
    nrows_length = from_sheet.nrows
    # 获取行数
    features = id_array
    # print features
    dataSet = [[] for i in range(0, (nrows_length - 1))]
    for var1 in range(1, nrows_length):
        temp = from_sheet.row_values(var1)
        for var2 in range(ncols_length):
            dataSet[var1 - 1].append(temp[var2])
    return dataSet, features

def createDataSet_iris():
    iris = datasets.load_iris()
    dataSet = []
    for var in iris.data:
        dataSet.append(list(var))
    targets = iris.target
    for index, var in enumerate(targets):
        dataSet[index].append(var)
        labels = ['a', 'b', 'c', 'd']
    return dataSet, labels


def createDataSet():
    # 导入数据，存入dataSet放课程分数以及该记录中目标课程是否大于75，大于存‘yes’反之‘no’;features放属性，即所有课程
    data = xlrd.open_workbook("dataset3.xlsx")
    from_sheet = data.sheet_by_index(0)
    # 通过索引获取sheet
    id_array = from_sheet.row_values(0)
    # 获取某行数据
    ncols_length = from_sheet.ncols
    # 获取列数
    nrows_length = from_sheet.nrows
    # 获取行数
    del id_array[0]
    del id_array[-1]
    # print id_array
    features = id_array
    dataSet = [[] for i in range(0, (nrows_length - 1))]
    # print len(dataSet)
    for var1 in range(1, nrows_length):
        temp = from_sheet.row_values(var1)
        for var2 in range(1, ncols_length):
            if temp[var2] >= '75':
                temp[var2] = '1'
            else:
                temp[var2] = '0'
            dataSet[var1 - 1].append(temp[var2])
    # print dataSet
    return dataSet, features  ##返回所有数据以及属性

# 选择最好的数据集(特征)划分方式  返回最佳特征下标
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1  # 特征个数
    baseEntropy = ig.calcShannonEnt(dataSet)
    bestInfoGainrate = 0.0
    bestFeature = -1
    for i in range(numFeatures):  # 遍历特征 第i个
        featureSet = set([example[i] for example in dataSet])  # 第i个特征取值集合
        newEntropy = 0.0
        splitinfo = 0.0
        for value in featureSet:
            subDataSet = ig.splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * ig.calcShannonEnt(subDataSet)  # 该特征划分所对应的entropy
            splitinfo -= prob * math.log(prob, 2)
        # print newEntropy, splitinfo
        infoGain = baseEntropy - newEntropy
        infoGainrate = float(infoGain) / float(splitinfo)
        if infoGainrate > bestInfoGainrate:
            bestInfoGainrate = infoGainrate
            bestFeature = i
    return bestFeature

def getCount(inputTree, dataSet, featLabels, count):
    # global num
    # print '+++++++', inputTree
    # print '11111+++', count
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    # count=[]
    for key in secondDict.keys():
        rightcount = 0
        wrongcount = 0
        tempfeatLabels = featLabels[:]
        subDataSet = ig.splitDataSet(dataSet, featIndex, key)
        tempfeatLabels.remove(firstStr)
        if type(secondDict[key]).__name__ == 'dict':
            getCount(secondDict[key], subDataSet, tempfeatLabels, count)
            # 在这里加上剪枝的代码，可以实现自底向上的悲观剪枝
        else:
            for eachdata in subDataSet:
                # print eachdata[-1]
                # print '//////////'
                # print secondDict[key]
                if str(eachdata[-1]) == str(secondDict[key]):
                    rightcount += 1
                else:
                    wrongcount += 1
            count.append([rightcount, wrongcount, secondDict[key]])
            # num+=rightcount+wrongcount


def getafterPruning(value, subDataSet):
    # 计算子树变作叶子节点后的误差率
    rightcount = 0
    wrongcount = 0
    for eachdata in subDataSet:
        if str(eachdata[-1]) == str(value):
            rightcount += 1
        else:
            wrongcount += 1
    return wrongcount, rightcount


def cutBranch_uptodown(inputTree, dataSet, featLabels):  # 自顶向下剪枝
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    print '=========='
    cc = 0
    for key in secondDict.keys():
        print '---', cc, '---'#, secondDict
        cc += 1

        if type(secondDict[key]).__name__ == 'dict':
            print key

            tempfeatLabels = featLabels[:]
            subDataSet = ig.splitDataSet(dataSet, featIndex, key)
            tempfeatLabels.remove(firstStr)
            tempcount = []
            getCount(secondDict[key], subDataSet, tempfeatLabels, tempcount)
            # 计算，并判断是否可以剪枝
            # 原误差率，显著因子取0.5
            tempnum = 0.0
            wrongnum = 0.0
            old = 0.0
            # 标准误差
            standwrong = 0.0
            wrongtemp = 1.0
            newtype = -1
            for var in tempcount:
                tempnum += var[0] + var[1]
                wrongnum += var[1]
                if float(var[1] + 0.5) / float(var[0] + var[1]) < wrongtemp:
                    # 求最小误差率，得出叶子节点对应目标结果newtype
                    wrongtemp = float(var[1] + 0.5) / float(var[0] + var[1])
                    newtype = var[-1]

            wrongAfterP, rightAfterP = getafterPruning(newtype, subDataSet)
            oldNum = float(wrongnum + 0.5 * len(tempcount))
            e = oldNum / float(tempnum)
            standwrong = math.sqrt(tempnum * e * (1 - e))
            # 假如剪枝
            new = float(wrongAfterP + 0.5) #/ float(wrongAfterP + rightAfterP)

            if new <= oldNum + standwrong and new >= oldNum - standwrong:  # 要确定新叶子结点的类别
                # 误判率最低的叶子节点的类为新叶子结点的类
                secondDict[key] = str(newtype)
            else:
                # 子树不剪，则继续下一个子树
                cutBranch_uptodown(secondDict[key], subDataSet, tempfeatLabels)


if __name__ == '__main__':
    global num
    num = 0
    # dataset, features = ig.createDataSet()
    # dataset,features = createDataSet()
    # dataset, features = createDataSet_iris()
    dataset, features = createDataSetCNDA(os.getcwd() + '/templates/tree/bloodpresure/bloodpresure.xls')
    # print dataset
    # print dataset
    print features
    features2 = features[:]  # labels2=labels：这样的赋值只是引用地址的传递，当labels改变时，labels2也会改变。只有labels2=labels[:]这样的才是真正的拷贝
    tree = tree.createTree(dataset, features, 'C4.5')

    # print tree
    # print classify(tree,features2,[0,1,1,1,0])
    tp.createPlot(tree)
    count = []
    # getCount(tree,dataset,features2,count)
    # print num
    # print count
    cutBranch_uptodown(tree, dataset, features2)
    # cutBranch_downtoup(tree, dataset, features2, count)
    tp.createPlot(tree)



def cutBranch_downtoup(inputTree, dataSet, featLabels, count):  # 自底向上剪枝
    # global num
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():  # 走到最深的非叶子结点
        if type(secondDict[key]).__name__ == 'dict':
            tempcount = []  # 本将的记录
            rightcount = 0
            wrongcount = 0
            tempfeatLabels = featLabels[:]
            subDataSet = ig.splitDataSet(dataSet, featIndex, key)
            tempfeatLabels.remove(firstStr)
            getCount(secondDict[key], subDataSet, tempfeatLabels, tempcount)
            # 将该分支上所有叶子节点以[正确数，错误数，节点]的形式存入tempcount中
            # 在这里加上剪枝的代码，可以实现自底向上的悲观剪枝
            # 计算，并判断是否可以剪枝
            # 原误差率，显著因子取0.5
            tempnum = 0.0
            wrongnum = 0.0
            old = 0.0
            # 标准误差
            standwrong = 0.0
            for var in tempcount:
                tempnum += var[0] + var[1]
                wrongnum += var[1]
            old = float(wrongnum + 0.5 * len(tempcount)) / float(tempnum)
            standwrong = math.sqrt(tempnum * old * (1 - old))
            # 假如剪枝
            new = float(wrongnum + 0.5) / float(tempnum)
            if new <= old + standwrong and new >= old - standwrong:  # 要确定新叶子结点的类别
                # 误判率最低的叶子节点的类为新叶子结点的类
                # 在count的每一个列表类型的元素里再加一个标记类别的元素。
                wrongtemp = 1.0
                newtype = -1
                for var in tempcount:
                    if float(var[1] + 0.5) / float(var[0] + var[1]) < wrongtemp:
                        wrongtemp = float(var[1] + 0.5) / float(var[0] + var[1])
                        newtype = var[-1]
                secondDict[key] = str(newtype)
                tempcount = []  # 这个有点复杂，因为如果发生剪枝，才会将它置空，如果不发生剪枝，那么应该保持原来的叶子结点的结构
            for var in tempcount:
                count.append(var)
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            continue
        rightcount = 0
        wrongcount = 0
        subDataSet = ig.splitDataSet(dataSet, featIndex, key)
        for eachdata in subDataSet:
            if str(eachdata[-1]) == str(secondDict[key]):
                rightcount += 1
            else:
                wrongcount += 1
        count.append([rightcount, wrongcount, secondDict[key]])  # 最后一个为该叶子结点的类别
