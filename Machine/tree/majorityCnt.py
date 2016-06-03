# -*- coding: utf-8 -*-
import operator

def majorityCnt(classList):
    # 多数表决
    # 按照类标签出现频率降序排序
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]