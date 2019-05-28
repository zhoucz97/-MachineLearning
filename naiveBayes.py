import numpy as np

def loadDataSet():
    """
    创建数据集,都是假的 fake data set
    :return: 单词列表posting_list, 所属类别class_vec
    """
    posting_list = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    class_vec = [0, 1, 0, 1, 0, 1]  # 1 is 侮辱性的文字, 0 is not
    return posting_list, class_vec


def createVocabList(dataSet):
    '''
    :param dataSet:
    :return:
    '''
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print('the word: {} is not in my vocabulary'.format(word))
    return returnVec


def train_naive_bayes(trainMartix, trainCategory):
    '''
    朴素贝叶斯分类函数
    :param: trainMartix: 向量矩阵
            trainCategory: 类别
    '''
    trainMartix_len = len(trainMartix)
    words_len = len(trainMartix[0])
    p0 = np.sum(trainCategory) / len(trainCategory)
    p0num = np.ones(words_len)
    p1num = np.ones(words_len)
    #p1num = p0num
    p0all = 2.0; p1all = 2.0
    for i in range(trainMartix_len):
        #如果是侮辱性句子
        if trainCategory[i] == 1:
            p0num += trainMartix[i]
            p0all += np.sum(trainMartix[i])
        else:
            p1num += trainMartix[i]
            p1all += np.sum(trainMartix[i])
    p0vec = np.log(p0num / p0all)
    p1vec = np.log(p1num / p1all)
    return p0vec, p1vec, p0

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p0 = sum(vec2Classify * p0Vec) + np.log(pClass1)
    p1 = sum(vec2Classify * p1Vec) + np.log(1-pClass1)
    if p0 > p1:
        return 1
    else:
        return 0


if "__main__" == __name__:
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    Martix = []
    Catecory = listClasses
    for i in range(len(listOPosts)):
        Martix.append(setOfWords2Vec(myVocabList, listOPosts[i]))
    p0vec, p1vec, p0 = train_naive_bayes(Martix, Catecory)
    test_one = ['love', 'my', 'dalmation']
    test_one_doc = np.array(setOfWords2Vec(myVocabList, test_one))
    print(test_one, 'classified as: ',classifyNB(test_one_doc, p0vec, p1vec, p0))
    test_two = ['stupid', 'garbage']
    test_two_doc = np.array(setOfWords2Vec(myVocabList, test_two))
    print(test_two, 'classified as: ', classifyNB(test_two_doc, p0vec, p1vec, p0))