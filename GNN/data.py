import os.path as osp
from collections import namedtuple
import numpy as np
import pandas as pd
from repo_data import get_repo_name
repo_name=get_repo_name()


Data = namedtuple('Data', ['x', 'y', 'adjacency_dict',
                           'train_mask', 'test_mask'])
'''
namedtuple是Python的collections模块中的一个工厂函数，它可以创建带有命名字段的元组子类。
你可以使用点号和字段名来访问namedtuple中的值，就像obj.attr一样。namedtuple和字典类似，
都包含了键值对，但是namedtuple还支持通过索引和迭代来访问，这是字典所不具备的功能。

namedtuple是一个Python模块，它可以创建一个不可变的和元组类似的数据结构，但是有字段名。
一个常见的例子是创建一个类来表示一个数学点。根据问题，你可能想要使用一个不可变的数据结构来表示一个给定的点。例如：
    from collections import namedtuple
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(1, 2)
    print(p.x) # 1
    print(p.y) # 2
这里，我们使用namedtuple()函数来创建一个名为Point的类，它有两个字段x和y。
然后我们用这个类来创建一个实例p，并用点号访问它的字段值。
'''


class GraphData(object):
    

    def __init__(self, data_root="./"):
        """
        数据可以通过属性 .data 获得，它将返回一个数据对象，包括如下几部分：
            * x: 节点的特征，维度为 15462 * 44，类型为 np.ndarray
            * y: 节点的标签，总共包括2个属性，类型为 np.ndarray
            * adjacency_dict: 邻接信息，，类型为 dict
            * train_mask: 训练集掩码向量，当节点属于训练集时，相应位置为True，否则False
            * test_mask: 测试集掩码向量，当节点属于测试集时，相应位置为True，否则False
        Args:
        -------
            data_root: string, optional
                存放数据的目录，原始数据路径: {data_root}/raw
                缓存数据路径: {data_root}/processed_cora.pkl
        """
     
        self.node_path=osp.join(data_root, "nodes_data_"+repo_name+"my.csv")
        self.edge_path=osp.join(data_root, "edges_data_"+repo_name+"my.csv")
      
        self._data = self.process_data()





    def process_data(self):
        """
        处理数据，得到节点特征和标签，邻接矩阵，训练集、验证集以及测试集
        """
        print("【GNN/data.py】Process data ...")

        nodes_data = pd.read_csv(self.node_path)
        edges_data = pd.read_csv(self.edge_path)

        ##节点特征  共有44个属性
        x = nodes_data[
                        ['author_experience' , 

                        'author_merge_ratio' , 
                        'author_changes_per_week' ,
                        'author_merge_ratio_in_project' ,
                        'total_change_num' ,
                        'author_review_num' ,

                        'is_reviewer' ,
                        'author_subsystem_change_num' ,
                        'author_subsystem_change_merge_ratio' ,
                        'author_avg_rounds' ,
                        'author_contribution_rate' ,

                        'author_merged_change_num' ,
                        'author_abandoned_changes_num' ,
                        'author_avg_duration' ,
                        'description_length' ,
                        'is_documentation' ,

                        'is_bug_fixing' ,
                        'is_feature' ,
                        'is_improve' ,
                        'is_refactor' ,
                        'commit_num' ,

                        'comment_num' ,
                        'comment_word_num' ,
                        'last_comment_mention' ,
                        'has_test_file' ,
                        'description_readability' ,

                        'is_responded' ,
                        'first_response_duration' ,
                        'project_changes_per_week' ,
                        'project_merge_ratio' ,
                        'changes_per_author' ,

                        'project_author_num' ,
                        'project_duration_per_merged_change' ,
                        'project_commits_per_merged_change' ,
                        'project_comments_per_merged_change' ,
                        'project_file_num_per_merged_change' ,

                        'project_churn_per_merged_change' ,
                        'project_duration_per_abandoned_change' ,
                        'project_commits_per_abandoned_change' ,
                        'project_comments_per_abandoned_change' ,
                        'project_file_num_per_abandoned_change' ,

                        'project_churn_per_abandoned_change' ,
                        'project_additions_per_week' ,
                        'project_deletions_per_week' ,
                        'workload' ,
                        'num_of_reviewers' ,

                        'num_of_bot_reviewers' ,
                        'avg_reviewer_experience' ,
                        'avg_reviewer_review_count' ,
                        'review_avg_rounds' ,
                        'review_avg_duration' ,

                        'lines_added' ,
                        'lines_updated',
                        'lines_deleted' ,
                        'files_added' ,
                        'files_deleted' ,

                        'files_modified' ,
                        'num_of_directory' ,
                        'modify_entropy' ,
                        'subsystem_num' ,
                        'language_num' ,

                        'file_type_num' ,
                        'segs_added' ,
                        'segs_deleted' ,
                        'segs_updated' ,
                        'modified_code_ratio' ,

                        'test_churn' ,
                        'src_churn' ,
                        'degree_centrality' ,
                        'closeness_centrality' ,
                        'betweenness_centrality' ,

                        'eigenvector_centrality' ,
                        'clustering_coefficient' ,
                        'k_coreness' ,
                        'avg_score' 
                         ]
                    ].to_numpy() #转成numpy类型
        
        ##预测标签
        # y = nodes_data[['status','time','rounds']].to_numpy()
        y = nodes_data[['status','time']].to_numpy()
        #是否被合入，响应速度，关闭速度

        # y = nodes_data[['close_speed']].to_numpy()
        
        
        # 读节点id->边
        edges_src = edges_data['SrcId'].to_numpy() #得到边的源结点
        edges_dst = edges_data['DesId'].to_numpy() #得到边的目标结点
        
        num_nodes = nodes_data.shape[0]  #得到结点数目

        # 80%作为训练集，20%作为测试集
        n_train = int(num_nodes * 0.8)
        train_mask = np.zeros(num_nodes, dtype=bool) 
        test_mask = np.zeros(num_nodes, dtype=bool)
        #创建一个长度为num_nodes的布尔数组，默认初始值为false，赋值给train_mask。
            
        # 划分的工具就是mask
        train_mask[:n_train] = True    #前80%为训练集
        test_mask[n_train:] = True     #后20%为测试集

        adjacency_dict=dict()

        # print("num_nodes====",num_nodes)
        # print("type(edges_src)====",type(edges_src))
        # print("edges_src.shape====",edges_src.shape)

        ##生成邻接表
        for i in range(num_nodes):
            adjacency_dict[i]=[]
        
        for i,srcId in enumerate(edges_src): #相当于搞一个idx++,记录序号
            # print("isis",i,srcId)
            # print("i=",i,end="  ")
            # print(srcId,end="  ")
            # print(edges_dst[i])
            adjacency_dict[srcId].append(edges_dst[i])
        # 这段代码的作用是遍历edges_src列表，对每个元素和它的索引进行操作。
        # edges_src和edges_dst是两个相同长度的列表，分别表示图中边的源节点和目标节点。
        # adjacency_dict是一个字典，键是节点，值是一个列表，表示与该节点相邻的节点。例如：
        '''
            edges_src = [0, 1, 2, 3]
            edges_dst = [1, 2, 3, 0]
            adjacency_dict = {0: [], 1: [], 2: [], 3: []}
        '''
        # 这表示有四个节点，编号为0到3，形成一个环路。代码的作用是把每条边的目标节点添加到源节点的邻接列表中，得到：
        # adjacency_dict = {0: [1], 1: [2], 2: [3], 3: [0]}
        # 这样就得到了每个节点的邻接信息。


        '''
        enumerate的用法
        fruits = ['apple', 'banana', 'orange']
        for i, fruit in enumerate(fruits):
            print(i, fruit)
            0 apple
            1 banana
            2 orange
        '''

        for i in range(num_nodes):
            if len(adjacency_dict[i])==0:
                adjacency_dict[i].append(i)        
        #这段代码的作用是遍历所有的节点，检查它们的邻接列表是否为空。如果为空，就把自己添加到邻接列表中。
        # 这样可以避免出现孤立的节点，或者在计算邻接矩阵时出现除以零的错误。


        ##打印图的基本信息
        print("【GNN/data.py】Node's feature shape: ", x.shape)
        print("【GNN/data.py】Node's label shape: ", y.shape)
        print("【GNN/data.py】Adjacency's shape: ", len(adjacency_dict))
        print("【GNN/data.py】Number of training nodes: ", train_mask.sum())
        print("【GNN/data.py】Number of test nodes: ", test_mask.sum())

        return Data(x=x, 
                    y=y, 
                    adjacency_dict=adjacency_dict,
                    train_mask=train_mask, 
                    test_mask=test_mask)

    @property
    def data(self):
        """返回Data数据对象，包括x, y, adjacency, train_mask, test_mask"""
        return self._data
    

# data=GraphData().data
# print(len(data.adjacency_dict))