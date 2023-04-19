import torch.nn as nn
# torch.nn是PyTorch的一个子模块，它提供了构建神经网络的基本组件，如层、激活函数、损失函数等。
# torch.nn中的所有组件都继承自Module类，这是一个抽象类，它定义了网络层的基本接口。
# torch.nn还支持多种设备和并行模式，如CPU、GPU、TPU等。
import torch
import torch.nn.functional as F
# torch.nn.functional模块包含了torch.nn库中的所有函数，如卷积、池化、激活函数、损失函数等。
# 这些函数可以直接对输入张量进行操作，而不需要创建Module对象。
from aggeregate import NeighborAggregator
# 是一种在Python中导入NeighborAggregator类的语句，这个类可能是自定义的或者来自于某个模块。
# 根据名称推测，NeighborAggregator类可能是用于实现图神经网络中的邻居聚合操作的
import torch.nn.init as init
# 是一种在Python中导入torch.nn.init模块的语句，通常用init作为别名。
# torch.nn.init模块提供了一些函数来初始化神经网络的参数，如权重和偏置。
# 这些函数可以根据不同的分布或方法来填充张量，如均匀分布、正态分布、xavier分布、正交矩阵等。


'''
class SageGCN(nn.Module):是一种定义一个类的语句，这个类继承了torch.nn.Module类，
表示它是一个神经网络模块。这个类的名字是SageGCN，表示它是一个基于GraphSAGE算法的图卷积网络层。这个类有以下几个参数：

input_dim: 输入特征的维度
hidden_dim: 隐层特征的维度
activation: 激活函数，默认为ReLU
aggr_neighbor_method: 邻居特征聚合方法，可选["mean", "sum", "max"]
aggr_hidden_method: 节点特征的更新方法，可选["sum", "concat"]
这个类的主要功能是根据邻居节点的特征和自身节点的特征来计算新的节点特征，具体过程如下：

1.使用NeighborAggregator模块来对邻居节点的特征进行聚合，得到neighbor_hidden
2.使用一个线性变换矩阵b来对自身节点的特征进行变换，得到self_hidden
3.根据aggr_hidden_method来对self_hidden和neighbor_hidden进行组合，得到hidden
4.如果有激活函数，则对hidden进行激活，否则直接返回hidden

'''


class SageGCN(nn.Module):  # 定义SageGCN类，继承自nn.Module
    def __init__(self, 
                 input_dim, # input_dim 表示输入特征的维度
                 hidden_dim, # hidden_dim 表示隐层特征的维度
                 activation=F.relu, # activation 表示激活函数,默认为 relu
                 aggr_neighbor_method="mean", # aggr_neighbor_method 表示邻居节点特征聚合的方法，可以选择 mean、sum 或 max
                 aggr_hidden_method="sum"): # aggr_hidden_method 表示隐层特征聚合的方法，可以选择 sum 或 concat
        # SageGCN 类的初始化函数

        #原本是mean和sum

        """SageGCN层定义
        Args:
            input_dim: 输入特征的维度
            hidden_dim: 隐层特征的维度，
                当aggr_hidden_method=sum, 输出维度为hidden_dim
                当aggr_hidden_method=concat, 输出维度为hidden_dim*2
            activation: 激活函数
            aggr_neighbor_method: 邻居特征聚合方法，["mean", "sum", "max"]
            aggr_hidden_method: 节点特征的更新方法，["sum", "concat"]
        """

        super(SageGCN, self).__init__()
        assert aggr_neighbor_method in ["mean", "sum", "max"]
        assert aggr_hidden_method in ["sum", "concat"]

        #assert aggr_neighbor_method in ["mean", "sum", "max"] 
        # 和 assert aggr_hidden_method in ["sum", "concat"]：判断输入的聚合方法是否合法。

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.aggr_neighbor_method = aggr_neighbor_method
        self.aggr_hidden_method = aggr_hidden_method
        self.activation = activation


        self.aggregator = NeighborAggregator(input_dim, 
                                             hidden_dim,
                                             aggr_method=aggr_neighbor_method)
        # 定义一个 NeighborAggregator 类的对象，用于聚合邻居节点的特征。


        ## 权重矩阵B
        self.b = nn.Parameter(torch.Tensor(input_dim, hidden_dim))
        # 定义一个参数 b，用于将输入特征转换为隐层特征。
        self.reset_parameters() #调用 reset_parameters 函数，对参数 b 进行初始化。

    
    def reset_parameters(self):
        init.kaiming_uniform_(self.b) #调用 reset_parameters 函数，对参数 b 进行初始化。

    def forward(self, src_node_features, neighbor_node_features,raw_data):#定义前向传播函数
        # src_node_features 表示源节点的输入特征
        # neighbor_node_features 表示邻居节点的输入特征
        # raw_data 表示额外的原始数据


        # 首先，使用 aggregator 对邻居节点特征进行聚合，得到 neighbor_hidden。
        # 然后，将源节点特征 src_node_features 与参数 b 相乘，得到 self_hidden。
        # 根据设定的隐层特征聚合方法，将 self_hidden 和 neighbor_hidden 进行合并，得到 hidden。
        # 最后，将 hidden 和 raw_data 进行拼接，得到最终的特征表示。
        # 如果设定了激活函数，则对特征表示进行激活，返回激活后的结果，否则返回未经过激活的结果。

        neighbor_hidden = self.aggregator(neighbor_node_features)

        self_hidden = torch.matmul(src_node_features, self.b)

        if self.aggr_hidden_method == "sum":  # 和 sum，直接相加
            hidden = self_hidden + neighbor_hidden
        elif self.aggr_hidden_method == "concat": # concat 连接，用torch.cat方法
            hidden = torch.cat([self_hidden, neighbor_hidden], dim=1)
        else:
            raise ValueError("Expected sum or concat, got {}"
                             .format(self.aggr_hidden))
        # print(hidden.size())
        # print(raw_data.size())
        hidden=torch.cat([hidden,raw_data],dim=1) #将 hidden 和 raw_data 进行拼接，得到最终的特征表示。
        # print(hidden.size())
        
        if self.activation:  #有激活函数就经过激活函数
            return self.activation(hidden)
        else:
            return hidden


    def extra_repr(self):
        #def extra_repr(self)额外的表示函数。
        # 返回一个字符串，表示该模块的  输入特征维度、输出特征维度 和 隐层特征聚合方法。

        #不是sum要把self.hidden_dim * 2
        output_dim = self.hidden_dim if self.aggr_hidden_method == "sum" else self.hidden_dim * 2

        return 'in_features={}, out_features={}, aggr_hidden_method={}'.format(
            self.input_dim, output_dim, self.aggr_hidden_method) #返回 输入特征维度、输出特征维度 和 隐层特征聚合方法



