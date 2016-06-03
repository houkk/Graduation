# -*- coding: utf-8 -*-
import xlrd
import numpy as np

def createDataSet(filePath):
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
    print features
    dataSet = [[] for i in range(0, (nrows_length - 1))]
    for var1 in range(1, nrows_length):
        temp = from_sheet.row_values(var1)
        for var2 in range(ncols_length):
            dataSet[var1 - 1].append(temp[var2])
    print dataSet

    return dataSet, features  ##返回所有数据以及属性

def createLabels(filePath):
    data = xlrd.open_workbook(filePath)
    from_sheet = data.sheet_by_index(0)
    # 通过索引获取sheet
    id_array = from_sheet.row_values(0)
    # 获取某行数据
    return id_array
# def main():
#     file = 'test1.xls'
#     createDataSet(file)
#
#
# if __name__ == '__main__':
#     main()