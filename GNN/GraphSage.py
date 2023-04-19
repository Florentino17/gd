import torch.nn as nn
from sageGCN import SageGCN
import torch
import torch.nn.init as init



class GraphSage(nn.Module):# 定义GraphSage神经网络
    def __init__(self, 
                 input_dim, 
                 hidden_dim,
                 num_neighbors_list): # 初始化函数，包括输入特征维度、隐藏层维度和每层邻居数量的列表
        
        super(GraphSage, self).__init__()
        self.input_dim = input_dim    #输入特征维度
        self.hidden_dim = hidden_dim  #隐藏层维度
        self.num_neighbors_list = num_neighbors_list  #每层邻居数量的列表

        self.num_layers = len(num_neighbors_list) # 计算图层数
        self.gcn = nn.ModuleList() # 使用ModuleList来存储多个GCN层

        # 每个GCN层都将上一层节点的特征作为输入，使用图卷积操作进行特征传播和更新，输出新的节点特征。
        # 添加第一层GCN层
        self.gcn.append(SageGCN(input_dim, hidden_dim[0]))

        # 添加其他GCN层，hidden_dim代表每层的隐藏层维度
        for index in range(0, len(hidden_dim) - 2): #遍历了从第二层到倒数第二层的所有层
            self.gcn.append(SageGCN(hidden_dim[index]+self.input_dim, hidden_dim[index+1]))
            # 上一层GCN输出的特征维度hidden_dim[index]加上44（可能是由于网络结构的需要，需要额外的44维特征输入），
            # 作为当前层GCN的输入维度。
            # 而hidden_dim[index+1] 则是当前层GCN的输出维度。这个循环的目的是为了将所有GCN层添加到网络中。

        # 最后一层不需要激活函数
        self.gcn.append(SageGCN(hidden_dim[-2]+self.input_dim, hidden_dim[-1], activation=None))
        #因为在节点分类任务中，输出层通常使用Softmax函数进行多分类，而Softmax函数通常与Cross-entropy loss损失函数一起使用，
        # 因此不需要在输出层添加激活函数。因此，该层使用了 None 作为激活函数参数。

        # 定义输出层，将隐藏层维度和44拼接成为输入维度
        self.fc=nn.Linear(hidden_dim[-1]+self.input_dim,1)
        # self.final_w=nn.Parameter(torch.Tensor(2*hidden_dim[-1],1))
        # init.kaiming_uniform_(self.final_w)


    def forward(self, node_features_list): # 前向传播函数，接受一个参数 node_features_list，用于存储节点特征的列表。
        d1=nn.Dropout(0.5)
        d2=nn.Dropout(0.1)  #用于进行网络训练时的随机失活操作，防止模型过拟合。
        hidden = node_features_list # 初始化特征列表
        raw_data = node_features_list # 用于保留原始数据，备份到变量 raw_data 中，以便后续使用。

        for l in range(self.num_layers):
            # 进入循环，循环次数为 num_layers，即神经网络中的层数。在每层循环中，
            # 首先创建一个空列表 next_hidden，用于存储当前层的特征结果。
            next_hidden = []   # 存储每层的特征
            gcn = self.gcn[l]  # 获取当前层的GCN层
            for hop in range(self.num_layers - l):
                # 获取当前层的 GCN 层，即图卷积层，并循环处理每一层的节点特征，即从当前层的节点特征开始，
                # 计算其与下一层的邻居节点特征之间的卷积运算，得到当前层的特征结果。

                src_node_features = hidden[hop] # 当前节点特征
                # print("l:",l,"hop:",hop,"src_node_features.shape:",src_node_features.shape)
                src_node_num = len(src_node_features) # 当前节点数量

                neighbor_node_features = hidden[hop + 1] \
                    .view((src_node_num, self.num_neighbors_list[hop], -1)) # 邻居节点特征
                
                # 调用GCN层进行运算，并保留原始数据
                h = gcn(src_node_features, neighbor_node_features,raw_data[hop])
                next_hidden.append(h) # 将计算得到的当前层特征结果存入 next_hidden 列表中，便于后续的处理。

            hidden = next_hidden # 当前层所有节点特征处理完毕后，将 next_hidden 赋值给 hidden，并进入下一层循环。
        
        result=hidden[0] # 获取最后一层的特征
        # result=torch.matmul(result,self.final_w)
        # result=torch.sigmoid(result)*4
        result=self.fc(result)  # 进行输出层的运算
        return result


    # 返回模型的输入特征和邻居节点数量列表
    def extra_repr(self):
        return 'in_features={}, num_neighbors_list={}'.format(
            self.input_dim, self.num_neighbors_list
        )



