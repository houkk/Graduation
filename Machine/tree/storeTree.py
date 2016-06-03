# -*- coding: utf-8 -*-
import pickle
import tree as tree
import infoGain as ig

def storeTree(myTree, routerPath, tree_name):
    fileName = routerPath + '/' + tree_name + '.txt'
    fw = open(fileName, 'w')
    pickle.dump(myTree, fw)
    fw.close()
    return fileName

def grabTree(filename):
    fr = open(filename)
    return pickle.load(fr)


# def main():
#     myDataSet, labels = ig.createDataSet()
#     myLabels = labels[:]
#     myTree = tree.createTree(myDataSet, labels)
#     # storeTree(myTree, 'tree.txt')
#     print grabTree('/home/mesogene/PycharmProjects/GraduationProject/templates/tree/test1/test1.txt')
#
# if __name__ == '__main__':
#     main()