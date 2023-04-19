import torch
import torch.nn as nn

import torch.nn.init as init


class NeighborAggregator(nn.Module):
    def __init__(self, 
                 input_dim, 
                 output_dim, 
                 use_bias=False, #是否使用偏置
                 aggr_method="mean"): #邻居聚合方式
        """聚合节点邻居
        Args:
            input_dim: 输入特征的维度
            output_dim: 输出特征的维度
            use_bias: 是否使用偏置 (default: {False})
            aggr_method: 邻居聚合方式 (default: {mean})
        """
        super(NeighborAggregator, self).__init__() # 调用父类的初始化方法

        self.input_dim = input_dim
        self.output_dim = output_dim
        self.use_bias = use_bias # 保存是否使用偏置项为属性
        self.aggr_method = aggr_method # 保存邻居聚合方式为属性

        self.weight = nn.Parameter(
            torch.Tensor(input_dim, output_dim)
            )  # 定义一个可学习的权重矩阵作为参数

        if self.use_bias:
            self.bias = nn.Parameter(
                torch.Tensor(self.output_dim)
                )  # 定义一个可学习的偏置向量作为参数
        self.reset_parameters()  # 调用重置参数的方法
    
    def reset_parameters(self):  # 定义一个重置参数的方法，用于初始化权重和偏置
        init.kaiming_uniform_(self.weight) # 使用kaiming均匀分布初始化权重矩阵
        #使用均匀分布来填充输入张量。这种方法可以使神经网络中的每一层激活函数的输出保持合理的方差，从而避免梯度爆炸或消失。
        
        if self.use_bias:
            init.zeros_(self.bias) # 如果使用偏置项,则使用全零初始化偏置向量

    def forward(self, neighbor_feature): # 定义前向传播的方法，接受邻居特征作为输入，返回聚合后的隐藏特征作为输出
        if self.aggr_method == "mean":  # 如果邻居聚合方式是"mean"
            aggr_neighbor = neighbor_feature.mean(dim=1) # 对邻居特征沿着第一维求平均值，得到每个节点的平均邻居特征
        elif self.aggr_method == "sum": # 如果邻居聚合方式是"sum"
            aggr_neighbor = neighbor_feature.sum(dim=1) #则沿着第一个维度计算邻居特征的总和
        elif self.aggr_method == "max":
            aggr_neighbor = neighbor_feature.max(dim=1).values # 如果聚合方法是最大值，则沿着第一个维度计算邻居特征的最大值
        else:
            raise ValueError("Unknown aggr type, expected sum, max, or mean, but got {}"
                             .format(self.aggr_method))  # 如果聚合方法是未知的，则抛出异常
        
        neighbor_hidden = torch.matmul(aggr_neighbor, self.weight)    # 将聚合后的邻居特征与权重矩阵相乘，得到隐藏层输出
        if self.use_bias:
            neighbor_hidden += self.bias # 如果使用偏置项，则将偏置向量加到隐藏层输出上

        return neighbor_hidden
 
    def extra_repr(self):  # 定义额外的表示函数，返回模型的输入维度、输出维度和聚合方法
        return 'in_features={}, out_features={}, aggr_method={}'.format(
            self.input_dim, self.output_dim, self.aggr_method)

