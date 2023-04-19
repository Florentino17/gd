from platform import node
import numpy as np
#          batch_src_index
def sampling(src_nodes, sample_num, neighbor_table,node_repre=None):


    # 根据源节点采样指定数量的邻居节点，注意这里用的是有放回的采样，
    # 某个节点的邻居节点数量少于采样数量时，采样结果出现重复的节点
    """  
    Arguments:
        src_nodes {list, ndarray} -- 源节点列表
        sample_num {int} -- 需要采样的节点数
        neighbor_table {dict} -- 节点到其邻居节点的映射表
    
    Returns:
        np.ndarray -- 采样结果构成的列表
    """
    results = []
    for sid in src_nodes:
        # 从节点的邻居中进行有放回地进行采样
        res = np.random.choice(neighbor_table[sid], size=(sample_num, ))
        # neighbor_table是总的邻居table，sid是对应的源节点id，sample_num为需要采样的结点数，不够则重复采样
        results.append(res)  #res包含四项内容，好像是一个[],三个arrary
    return np.asarray(results).flatten()
    #results是一个列表类型，所以先转成numpy类型（array或者mat）

#.flatten()：NumPy的一个方法，返回将数组展平为一维数组的副本。
# 换句话说，它通过将数组的所有元素连接成单个长数组，将多维数组转换为一维数组。




def multihop_sampling(src_nodes, sample_nums, neighbor_table,node_repre=None):
    """根据源节点进行多阶采样
    
    Arguments:
        src_nodes {list, np.ndarray} -- 源节点id
        sample_nums {list of int} -- 每一阶需要采样的个数
        neighbor_table {dict} -- 节点到其邻居节点的映射
    
    Returns:
        [list of ndarray] -- 每一阶采样的结果
    """
    repre=node_repre
    sampling_result = [src_nodes]
    for k, hopk_num in enumerate(sample_nums):
        hopk_result = sampling(sampling_result[k], hopk_num, neighbor_table,repre)
        #采样的源节点是上一阶采样的结果sampling_result[k]
        sampling_result.append(hopk_result)
        #每一阶采样后的结果hopk_result被添加到sampling_result中。
        #最终返回sampling_result，其中每一阶的采样结果都保存在sampling_result的一个元素中。
    return sampling_result



