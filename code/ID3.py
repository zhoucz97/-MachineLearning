'''
ID3
机器学习实战之决策树
2019-4-26
zcz
'''
import operator
from math import log
import matplotlib.pyplot as plt
'''
decisionNode = dict(boxstype='sawtooth', fc='0.8')
leafNode = dict(boxstyle='round4')'''

def createDataSet():
    '''
    数据初始化
    :return:
    '''
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


def calcShannonEnt(dataSet):
    '''
    计算数据集的香农熵
    :param dataSet:
    :return:
    '''
    #计算数据集长度,ji个数
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        #为所有可能的分类创建字典
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 1
        else:
            labelCounts[currentLabel] += 1
    #香农熵
    shannonEnt = 0.0
    for key in labelCounts:
        #计算频率先
        prob = float(labelCounts[key])/numEntries
        #计算香农熵
        shannonEnt -= prob * log(prob, 2)
    #熵越高，混合的数据越多
    return shannonEnt

def splitDataSet(dataSet, axis, value):
    '''
    按照给定特征axis划分数据集,axis维度的数据如果与value相等，则加入
    :param dataSet:
    :param axis:
    :param value:
    :return:
    '''
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        #在第i维中把所有的可能取值找出，然后用set去重
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        #新熵值
        newEntropy = 0.0
        #计算每种划分方式的信息熵
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        #infoGain>bestInfoGain说明熵减少，无序度降低
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    '''
    函数使用分类名称的列表，创建键值为classList中唯一值的数据字典，
    存储了classList中每个类标签出现的频率，最后返回出现次数最多的分类名称
    :param classList:
    :return:
    '''
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    #sorted()函数： 第一个参数将字典里的所有返回到迭代器， key表示以迭代器里的第一个元素排序
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    #类别
    classList = [example[-1] for example in dataSet]
    #类别完全一致，则停止划分
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    #遍历完所有特征时返回出现次数最多的类型
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    #最优特征值
    bestFeat = chooseBestFeatureToSplit(dataSet)
    #最优特征值所对应的标签
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    #得到列表包含的所有属性值
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree



if __name__ == '__main__':
    myDat, lables = createDataSet()
    print(myDat)
    '''print(calcShannonEnt(myDat))
    print('-----------')
    print(splitDataSet(myDat, 0, 1))
    print('-----------')'''
    print(chooseBestFeatureToSplit(myDat))
    print('-----------')
    myTree = createTree(myDat, lables)
    print(myTree)