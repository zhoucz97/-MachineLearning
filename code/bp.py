import random
from functools import reduce
from numpy import *

# sigmoid 函数
def sigmoid(inX):
    '''
    Desc:
        sigmoid 函数实现
    Args:
        inX --- 输入向量
    Returns:
        对输入向量作用 sigmoid 函数之后得到的输出
    '''
    return 1.0 / (1 + exp(-inX))


# 定义神经网络的节点类
class Node(object):
    '''
    Desc:
        神经网络的节点类
    '''
    def __init__(self, layer_index, node_index):
        '''
        Desc:
            初始化一个节点
        Args:
            layer_index --- 层的索引，也就是表示第几层
            node_index --- 节点的索引，也就是表示节点的索引
        Returns:
            None
        '''
        # 设置节点所在的层的位置
        self.layer_index = layer_index
        # 设置层中的节点的索引
        self.node_index = node_index
        # 设置此节点的下游节点，也就是这个节点与下一层的哪个节点相连
        self.downstream = []
        # 设置此节点的上游节点，也就是哪几个节点的下游节点与此节点相连
        self.upstream = []
        # 此节点的输出
        self.output = 0
        # 此节点真实值与计算值之间的差值
        self.delta = 0

    def set_output(self, output):
        '''
        Desc:
            设置节点的 output
        Args:
            output --- 节点的 output
        Returns:
            None
        '''
        self.output = output

    def append_downstream_connection(self, conn):
        '''
        Desc:
           添加此节点的下游节点的连接
        Args:
            conn --- 当前节点的下游节点的连接的 list
        Returns:
            None
        '''
        # 使用 list 的 append 方法来将 conn 中的节点添加到 downstream 中
        self.downstream.append(conn)

    def append_upstream_connection(self, conn):
        '''
        Desc:
            添加此节点的上游节点的连接
        Args:
            conn ---- 当前节点的上游节点的连接的 list
        Returns:
            None
        '''
        # 使用 list 的 append 方法来将 conn 中的节点添加到 upstream 中
        self.upstream.append(conn)

    def calc_output(self):
        '''
        Desc:
            计算节点的输出，依据 output = sigmoid(wTx)
        Args:
            None
        Returns:
            None
        '''
        # 使用 reduce() 函数对其中的因素求和
        output = reduce(lambda ret, conn: ret + conn.upstream_node.output * conn.weight, self.upstream, 0)
        # 对上游节点的 output 乘 weights 之后求和得到的结果应用 sigmoid 函数，得到当前节点的 output
        self.output = sigmoid(output)

    def calc_hidden_layer_delta(self):
        '''
        Desc:
            计算隐藏层的节点的 delta
        Args:
            output --- 节点的 output
        Returns:
            None
        '''
        # 根据 https://www.zybuluo.com/hanbingtao/note/476663 的 式4 计算隐藏层的delta
        downstream_delta = reduce(lambda ret, conn: ret + conn.downstream_node.delta * conn.weight, self.downstream, 0.0)
        # 计算此节点的 delta
        self.delta = self.output * (1 - self.output) * downstream_delta

    def calc_output_layer_delta(self, label):
        '''
        Desc:
            计算输出层的 delta
        Args:
            label --- 输入向量对应的真实标签，不是计算得到的结果
        Returns:
            None
        '''
        # 就是那输出层的 delta
        self.delta = self.output * (1 - self.output) * (label - self.output)

    def __str__(self):
        '''
        Desc:
            将节点的信息打印出来
        Args:
            None
        Returns:
            None
        '''
        # 打印格式：第几层 - 第几个节点，output 是多少，delta 是多少
        node_str = '%u-%u: output: %f delta: %f' % (self.layer_index, self.node_index, self.output, self.delta)
        # 下游节点
        downstream_str = reduce(lambda ret, conn: ret + '\n\t' + str(conn), self.downstream, '')
        # 上游节点
        upstream_str = reduce(lambda ret, conn: ret + '\n\t' + str(conn), self.upstream, '')
        # 将本节点 + 下游节点 + 上游节点 的信息打印出来
        return node_str + '\n\tdownstream:' + downstream_str + '\n\tupstream:' + upstream_str


# ConstNode 对象，为了实现一个输出恒为 1 的节点（计算偏置项 wb 时需要）
class ConstNode(object):
    '''
    Desc:
        常数项对象，即相当于计算的时候的偏置项
    '''
    def __init__(self, layer_index, node_index):
        '''
        Desc:
            初始化节点对象
        Args:
            layer_index --- 节点所属的层的编号
            node_index --- 节点的编号
        Returns:
            None
        '''
        self.layer_index = layer_index
        self.node_index = node_index
        self.downstream = []
        self.output = 1


    def append_downstream_connection(self, conn):
        '''
        Desc:
            添加一个到下游节点的连接
        Args:
            conn --- 到下游节点的连接
        Returns:
            None
        '''
        # 使用 list 的 append 方法将包含下游节点的 conn 添加到 downstream 中
        self.downstream.append(conn)


    def calc_hidden_layer_delta(self):
        '''
        Desc:
            计算隐藏层的 delta
        Args:
            None
        Returns:
            None
        '''
        # 使用我们的 公式 4 来计算下游节点的 delta，求和
        downstream_delta = reduce(lambda ret, conn: ret + conn.downstream_node.delta * conn.weight, self.downstream, 0.0)
        # 计算隐藏层的本节点的 delta
        self.delta = self.output * (1 - self.output) * downstream_delta


    def __str__(self):
        '''
        Desc:
           将节点信息打印出来
        Args:
            None
        Returns:
            None
        '''
        # 将节点的信息打印出来
        # 格式 第几层-第几个节点的 output
        node_str = '%u-%u: output: 1' % (self.layer_index, self.node_index)
        # 此节点的下游节点的信息
        downstream_str = reduce(lambda ret, conn: ret + '\n\t' + str(conn), self.downstream, '')
        # 将此节点与下游节点的信息组合，一起打印出来
        return node_str + '\n\tdownstream:' + downstream_str


# 神经网络的层对象，负责初始化一层。此外，作为 Node 的集合对象，提供对 Node 集合的操作
class Layer(object):
    '''
    Desc:
        神经网络的 Layer 类
    '''

    def __init__(self, layer_index, node_count):
        '''
        Desc:
            神经网络的层对象的初始化
        Args:
            layer_index --- 层的索引
            node_count --- 节点的个数
        Returns:
            None
        '''
        # 设置 层的索引
        self.layer_index = layer_index
        # 设置层中的节点的 list
        self.nodes = []
        # 将 Node 节点添加到 nodes 中
        for i in range(node_count):
            self.nodes.append(Node(layer_index, i))
        # 将 ConstNode 节点也添加到 nodes 中
        self.nodes.append(ConstNode(layer_index, node_count))

    def set_output(self, data):
        '''
        Desc:
            设置层的输出，当层是输入层时会用到
        Args:
            data --- 输出的值的 list
        Returns:
            None
        '''
        # 设置输入层中各个节点的 output
        for i in range(len(data)):
            self.nodes[i].set_output(data[i])

    def calc_output(self):
        '''
        Desc:
            计算层的输出向量
        Args:
            None
        Returns:
            None
        '''
        # 遍历本层的所有节点（除去最后一个节点，因为它是恒为常数的偏置项b）
        # 调用节点的 calc_output 方法来计算输出向量
        for node in self.nodes[:-1]:
            node.calc_output()

    def dump(self):
        '''
        Desc:
            将层信息打印出来
        Args:
            None
        Returns:
            None
        '''
        # 遍历层的所有的节点 nodes，将节点信息打印出来
        for node in self.nodes:
            print(node)


# Connection 对象类，主要负责记录连接的权重，以及这个连接所关联的上下游的节点
class Connection(object):
    '''
    Desc:
        Connection 对象，记录连接权重和连接所关联的上下游节点，注意，这里的 connection 没有 s ，不是复数
    '''
    def __init__(self, upstream_node, downstream_node):
        '''
        Desc:
            初始化 Connection 对象
        Args:
            upstream_node --- 上游节点
            downstream_node --- 下游节点
        Returns:
            None
        '''
        # 设置上游节点
        self.upstream_node = upstream_node
        # 设置下游节点
        self.downstream_node = downstream_node
        # 设置权重，这里设置的权重是 -0.1 到 0.1 之间的任何数
        self.weight = random.uniform(-0.1, 0.1)
        # 设置梯度 为 0.0
        self.gradient = 0.0

    def calc_gradient(self):
        '''
        Desc:
            计算梯度
        Args:
            None
        Returns:
            None
        '''
        # 下游节点的 delta * 上游节点的 output 计算得到梯度
        self.gradient = self.downstream_node.delta * self.upstream_node.output

    def update_weight(self, rate):
        '''
        Desc:
            根据梯度下降算法更新权重
        Args:
            rate --- 学习率 / 或者成为步长
        Returns:
            None
        '''
        # 调用计算梯度的函数来将梯度计算出来
        self.calc_gradient()
        # 使用梯度下降算法来更新权重
        self.weight += rate * self.gradient

    def get_gradient(self):
        '''
        Desc:
            获取当前的梯度
        Args:
            None
        Returns:
            当前的梯度 gradient
        '''
        return self.gradient

    def __str__(self):
        '''
        Desc:
            将连接信息打印出来
        Args:
            None
        Returns:
            连接信息进行返回
        '''
        # 格式为：上游节点的层的索引+上游节点的节点索引 ---> 下游节点的层的索引+下游节点的节点索引，最后一个数是权重
        return '(%u-%u) -> (%u-%u) = %f' % (
            self.upstream_node.layer_index,
            self.upstream_node.node_index,
            self.downstream_node.layer_index,
            self.downstream_node.node_index,
            self.weight)



# Connections 对象，提供 Connection 集合操作。
class Connections(object):
    '''
    Desc:
        Connections 对象，提供 Connection 集合的操作，看清楚后面有没有 s ，不要看错
    '''
    def __init__(self):
        '''
        Desc:
            初始化 Connections 对象
        Args:
            None
        Returns:
            None
        '''
        # 初始化一个列表 list
        self.connections = []

    def add_connection(self, connection):
        '''
        Desc:
            将 connection 中的节点信息 append 到 connections 中
        Args:
            None
        Returns:
            None
        '''
        self.connections.append(connection)

    def dump(self):
        '''
        Desc:
            将 Connections 的节点信息打印出来
        Args:
            None
        Returns:
            None
        '''
        for conn in self.connections:
            print(conn)


# Network 对象，提供相应 API
class Network(object):
    '''
    Desc:
        Network 类
    '''
    def __init__(self, layers):
        '''
        Desc:
            初始化一个全连接神经网络
        Args:
            layers --- 二维数组，描述神经网络的每层节点数
        Returns:
            None
        '''
        # 初始化 connections，使用的是 Connections 对象
        self.connections = Connections()
        # 初始化 layers
        self.layers = []
        # 我们的神经网络的层数
        layer_count = len(layers)
        # 节点数
        node_count = 0
        # 遍历所有的层，将每层信息添加到 layers 中去
        for i in range(layer_count):
            self.layers.append(Layer(i, layers[i]))
        # 遍历除去输出层之外的所有层，将连接信息添加到 connections 对象中
        for layer in range(layer_count - 1):
            connections = [Connection(upstream_node, downstream_node) for upstream_node in self.layers[layer].nodes for downstream_node in self.layers[layer + 1].nodes[:-1]]
            # 遍历 connections，将 conn 添加到 connections 中
            for conn in connections:
                self.connections.add_connection(conn)
                # 为下游节点添加上游节点为 conn
                conn.downstream_node.append_upstream_connection(conn)
                # 为上游节点添加下游节点为 conn
                conn.upstream_node.append_downstream_connection(conn)


    def train(self, labels, data_set, rate, epoch):
        '''
        Desc:
            训练神经网络
        Args:
            labels --- 数组，训练样本标签，每个元素是一个样本的标签
            data_set --- 二维数组，训练样本的特征数据。每行数据是一个样本的特征
            rate --- 学习率
            epoch --- 迭代次数
        Returns:
            None
        '''
        # 循环迭代 epoch 次
        for i in range(epoch):
            # 遍历每个训练样本
            for d in range(len(data_set)):
                # 使用此样本进行训练（一条样本进行训练）
                self.train_one_sample(labels[d], data_set[d], rate)
                # print 'sample %d training finished' % d

    def train_one_sample(self, label, sample, rate):
        '''
        Desc:
            内部函数，使用一个样本对网络进行训练
        Args:
            label --- 样本的标签
            sample --- 样本的特征
            rate --- 学习率
        Returns:
            None
        '''
        # 调用 Network 的 predict 方法，对这个样本进行预测
        self.predict(sample)
        # 计算根据此样本得到的结果的 delta
        self.calc_delta(label)
        # 更新权重
        self.update_weight(rate)

    def calc_delta(self, label):
        '''
        Desc:
            计算每个节点的 delta
        Args:
            label --- 样本的真实值，也就是样本的标签
        Returns:
            None
        '''
        # 获取输出层的所有节点
        output_nodes = self.layers[-1].nodes
        # 遍历所有的 label
        for i in range(len(label)):
            # 计算输出层节点的 delta
            output_nodes[i].calc_output_layer_delta(label[i])
        # 这个用法就是切片的用法， [-2::-1] 就是将 layers 这个数组倒过来，从没倒过来的时候的倒数第二个元素开始，到翻转过来的倒数第一个数，比如这样：aaa = [1,2,3,4,5,6,7,8,9],bbb = aaa[-2::-1] ==> bbb = [8, 7, 6, 5, 4, 3, 2, 1]
        # 实际上就是除掉输出层之外的所有层按照相反的顺序进行遍历
        for layer in self.layers[-2::-1]:
            # 遍历每层的所有节点
            for node in layer.nodes:
                # 计算隐藏层的 delta
                node.calc_hidden_layer_delta()

    def update_weight(self, rate):
        '''
        Desc:
            更新每个连接的权重
        Args:
            rate --- 学习率
        Returns:
            None
        '''
        # 按照正常顺序遍历除了输出层的层
        for layer in self.layers[:-1]:
            # 遍历每层的所有节点
            for node in layer.nodes:
                # 遍历节点的下游节点
                for conn in node.downstream:
                    # 根据下游节点来更新连接的权重
                    conn.update_weight(rate)

    def calc_gradient(self):
        '''
        Desc:
            计算每个连接的梯度
        Args:
            None
        Returns:
            None
        '''
        # 按照正常顺序遍历除了输出层之外的层
        for layer in self.layers[:-1]:
            # 遍历层中的所有节点
            for node in layer.nodes:
                # 遍历节点的下游节点
                for conn in node.downstream:
                    # 计算梯度
                    conn.calc_gradient()

    def get_gradient(self, label, sample):
        '''
        Desc:
            获得网络在一个样本下，每个连接上的梯度
        Args:
            label --- 样本标签
            sample --- 样本特征
        Returns:
            None
        '''
        # 调用 predict() 方法，利用样本的特征数据对样本进行预测
        self.predict(sample)
        # 计算 delta
        self.calc_delta(label)
        # 计算梯度
        self.calc_gradient()

    def predict(self, sample):
        '''
        Desc:
            根据输入的样本预测输出值
        Args:
            sample --- 数组，样本的特征，也就是网络的输入向量
        Returns:
            使用我们的感知器规则计算网络的输出
        '''
        # 首先为输入层设置输出值output为样本的输入向量，即不发生任何变化
        self.layers[0].set_output(sample)
        # 遍历除去输入层开始到最后一层
        for i in range(1, len(self.layers)):
            # 计算 output
            self.layers[i].calc_output()
        # 将计算得到的输出，也就是我们的预测值返回
        return list(map(lambda node: node.output, self.layers[-1].nodes[:-1]))

    def dump(self):
        '''
        Desc:
            打印出我们的网络信息
        Args:
            None
        Returns:
            None
        '''
        # 遍历所有的 layers
        for layer in self.layers:
            # 将所有的层的信息打印出来
            layer.dump()




def train_data_set():
    '''
    获取训练数据
    以异或为例
    :return:
    '''
    labels = [[1],[0],[1],[0]]
    data_set = [[0,1],
                [0,0],
                [1,0],
                [1,1]]
    return labels, data_set



if "__main__" == __name__:
    #初始化神经网络
    net = Network([2,3,1])
    #获取训练数据
    labels, data_set = train_data_set()
    labels = list(labels)
    data_set = list(data_set)
    #调用Network的train进行训练
    net.train(labels, data_set, 0.3, 5000)
    net.dump()
    print(net.predict([1,0]))
