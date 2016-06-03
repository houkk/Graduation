# -*- coding: utf-8 -*-
import majorityCnt as mc
import infoGain as ig
import C45 as C45


def createTree(dataSet, labels, classify):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        # 只有一个类别
        return classList[0]
    if len(dataSet[0]) == 1:
        # 多数表决
        return mc.majorityCnt(classList)
    if classify == "C4.5":
        bestFeat = C45.chooseBestFeatureToSplit(dataSet)
    else:
        bestFeat = ig.choseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]

    del(labels[bestFeat])

    myTree = {bestFeatLabel: {}}
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)

    for values in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][values] = createTree(
            ig.splitDataSet(dataSet, bestFeat, values),
            subLabels,
            classify
        )

    return myTree
