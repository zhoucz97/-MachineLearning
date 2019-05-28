def loadDataSet():
    '''简单的数据集'''
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


def initialCandidateSet(dataSet):
    '''构建初始候选项集'''
    ICS = []
    for transaction in dataSet:
        for it in transaction:
            if [it] not in ICS:
                ICS.append([it])
    return list(map(frozenset, ICS))


def getItemSet(dataSet, ICS):
    # 得到频繁项集
    FS = {}
    # dataSet =
    for transaction in dataSet:
        for i in ICS:
            if set(i) <= set(transaction):
                if i not in FS:
                    FS[i] = 1
                else:
                    FS[i] += 1
    return FS  # 字典类型


def getItemAndSupport(FS, dataSet, minSupport):
    '''计算项集的支持度'''
    List = []
    supportData = {}
    len_dataSet = float(len(dataSet))
    for i in FS:
        support = FS[i] / len_dataSet
        if support >= minSupport:
            # 去除支持度小于最小支持度的项集，即将满足条件的项集加入新列表
            List.insert(0, i)
        # 记录每个的支持度
        supportData[i] = support
    return List, supportData


def newItemSet(L, k):
    '''组合新项集'''
    '''k表示生成的新项集中所含有的元素个数'''
    newList = []
    len_nL = len(L)
    for i in range(len_nL):
        for j in range(i + 1, len_nL):
            L1 = list(L[i])[:k - 2]
            L2 = list(L[j])[:k - 2]
            if L1 == L2:
                # 由频繁k项集得到频繁k+1项集，两个列表前k-2项相等，才会得到频繁二项集
                newList.append(L[i] | L[j])
    return newList


def apriori(dataSet, minSupport):
    # 构建初始候选项集
    ICS = initialCandidateSet(dataSet)
    # print(ICS)
    # 得到初始频繁项集（即频繁一项集) dir类型
    FS = getItemSet(dataSet, ICS)
    # print(FS)
    # 得到筛选后的频繁项集和支持度
    List, supportData = getItemAndSupport(FS, dataSet, minSupport)
    # print(List,supportData)
    # L 用来保存每次的频繁项集
    L = [List]
    # 从频繁二项集开始循环
    k = 2
    while (len(L[k - 2]) > 1):
        # 组合新项集
        newIS = newItemSet(L[k - 2], k)
        # print(newIS)
        newFS = getItemSet(dataSet, newIS)
        newList, newSupportData = getItemAndSupport(newFS, dataSet, minSupport)
        # 将新项集的支持度数据加入原有数据中
        supportData.update(newSupportData)
        # 将符合最小支持度的项集加入L
        L.append(newList)
        k += 1
    return L, supportData


if __name__ == '__main__':
    # 得到数据集
    myData = loadDataSet()
    L, supportData = apriori(myData, 0.3)
    print('频繁项集：')
    for i in L:
        print(i)
    print('支持度信息：')
    for i in supportData:
        print(i, ':', supportData[i])