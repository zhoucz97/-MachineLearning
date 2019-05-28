from numpy import *

def loadDataSet(filename):
    '''
    读取数据集
    '''
    dataMat = []
    fr = open(filename)
    #读取文件所有行
    lines = fr.readlines()
    for line in lines:
        line = line.strip().split('\t')
        line = list(map(float, line))
        dataMat.append(line)
    return dataMat


def distEclud(vecA, vecB):
    '''计算欧式距离'''
    #print(vecA)
    return sqrt(sum(power(vecA - vecB, 2)))

def randCent(dataSet, k):
    '''构建簇质心'''
    #shape函数为查看矩阵的维数，shape[0]为第二维，shape[1]为第一维
    n = shape(dataSet)[1]
    centroids = mat( zeros((k,n)) )
    for j in range(n):
        minJ = min(dataSet[:, j])
        maxJ = max(dataSet[:, j])
        # 得到该列数据的范围(最大值-最小值)
        rangeJ = float(max(dataSet[:, j]) - minJ)
        # k个质心向量的第j维数据值随机为位于(最小值，最大值)内的某一值
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
    #返回k*1的随机数列表
    return centroids


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    #获取样本数据集个数
    m = shape(dataSet)[0]
    #初始化矩阵，判断数据属于哪个簇,存放了索引值和距离的平方
    clusterAssment = mat(zeros((m, 2)))
    #初始化K个质心向量
    centroids = createCent(dataSet, k)
    #判断聚类结果是否发生变化
    clusterChanged = True
    while clusterChanged:
        #遍历数据集
        clusterChanged = False
        for i in range(m):
            # 初始化距离和索引
            minDist = inf; minIndex= -1
            for j in range(k):
                #计算数据与当前质心的距离
                #print(dataSet[i, :])
                dist = distMeas(dataSet[i, :], centroids[j, :])
                #如果当前距离为目前最小
                if dist < minDist:
                    minDist=dist
                    minIndex=j
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, 0] = minIndex
            clusterAssment[i, 1] = minDist**2

        print(centroids)

        #根据新质心重新聚类
        for cent in range(k):
            #关于nonzero的使用
            #https://blog.csdn.net/ruibin_cao/article/details/83242489
            #https://blog.csdn.net/xinjieyuan/article/details/81477120
            #nonzero返回含有两个array的truple,一个array为行值，一个为列值
            #此代码为找出clusterAssment中第一列即最小索引，等于cent的数据，nonzero之后得到符合条件的数据的行值，再根据行值从dataSet中挑选数据
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A==cent)[0]]
            #计算这些数据的均值，作为新的质心,mean()用来计算列的平均值
            centroids[cent, :] = mean(ptsInClust, 0)

    return centroids, clusterAssment

if "__main__" == __name__:
    filename = r"E:\machinelearninginaction-master\Ch10\testSet.txt"
    #mat为生成矩阵
    dataMat = mat(loadDataSet(filename))
    myCentroids, clustAssing = kMeans(dataMat, 4)
    print(clustAssing)

