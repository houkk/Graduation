# -*- coding: utf-8 -*-
import tree as tree
import infoGain as ig

def classify(myTree, featLabels, testVec):
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    featIndex = featLabels.index(firstStr)

    for key in secondDict:
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

def bloodPresure(myTree, featLabels, testVec):
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    featIndex = featLabels.index(firstStr)

# def main():
#     myDataSet, labels = ig.createDataSet()
#     myLabels = labels[:]
#     myTree = tree.createTree(myDataSet, labels)
#     print classify(myTree, myLabels, [1, 0])
#
# if __name__ == '__main__':
#     main()