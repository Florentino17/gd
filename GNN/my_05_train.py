from cmath import nan
from tkinter import Variable
from sympy import im
import torch
import sys
import os
import torch.nn.functional as F
sys.path.append(os.getcwd())
import numpy as np
import torch.nn as nn
import torch.optim as optim
from GraphSage import GraphSage
from GNN.data import GraphData
from sample import multihop_sampling
from day_split_data import day_open_pr_id
from eval_index.Kendall_tau_distance import kendall_tau_distance
from eval_index.mrr import mrr
from repo_data import get_repo_name
from eval_index.ndcg import ndcg as NDCG
from util.path_exist import path_exists_or_create
repo_name=get_repo_name()




def my_05_train_process():

    def listnet_loss(y_i, z_i):
        """
        y_i: (n_i, 1) 维度
        z_i: (n_i, 1)
        """

        P_y_i = F.softmax(y_i, dim=0)
        # P_y_i 是一个 y_i 行 1 列的张量，表示第 i 个查询下的 y_i 个pr的真实优先级概率分布
        P_z_i = F.softmax(z_i, dim=0) 
        # P_z_i 是一个 z_i 行 1 列的张量，表示第 i 个查询下的 z_i 个pr的预测优先级概率分布

        # P_y_i = prob(y_i)
        # P_z_i = prob(z_i)
        return - torch.sum(P_y_i * torch.log(P_z_i))
        # 返回第 i 个查询下真实优先级概率分布和预测优先级概率分布之间的交叉熵损失函数值
        # L = -1/n ∑j=1^n y_j ln a_j  其中，n是样本数，y_j是第j个样本的真实标签，a_j是第j个样本的预测概率

    def pair_loss(y_pred, y_true):
        # loss=torch.tensor(0.0,requires_grad=True)
        # for i in range(len(y_true)):
        #     for j in range(i+1,len(y_true)):
        #         if y_true[i]>y_true[j] and y_pred[i]<y_pred[j]:
        #             loss=loss+1
        #         elif y_true[i]<y_true[j] and y_pred[i]>y_pred[j]:
        #             loss=loss+1
        #         else:
        #             continue
        
        # return loss
        loss=torch.tensor(0.0,requires_grad=True)
        for i in range(len(y_true)):
            for j in range(i+1,len(y_true)):
                if y_true[i]==y_true[j]:
                    loss=loss+abs(y_pred[i]-y_pred[j])
                else:
                    t=(y_pred[i]-y_pred[j])/(y_true[i]-y_true[j])
                    if t<1:
                        loss=loss+1-t
                    else:
                        continue
    
        return loss

        # loss=torch.tensor(0.0,requires_grad=True)
        # for i in range(len(y_true)):
        #     for j in range(i+1,len(y_true)):
        #         if y_true[i]==y_true[j]:
        #             loss=loss+abs(y_pred[i]-y_pred[j])
        #         else:
        #             t=(y_pred[i]-y_pred[j])/(y_true[i]-y_true[j])
        #             if t<1:
        #                 loss=loss+1-t
        #             else:
        #                 continue
        
        # return loss
    

    def priority_loss(y_pred, y_true, k=None):
        y_true=F.softmax(y_true, dim=0)
        y_pred=F.softmax(y_pred, dim=0)
        y_true, indices = y_true.sort(descending=True, dim=-1)
        if k is not None:
            if k<=len(y_true):
                indices=indices[:k]
        y=y_true[:k]
        pred_sorted_by_true = y_pred.gather(dim=0, index=indices)

        criterion=nn.MSELoss(reduction='mean')

        loss=criterion(pred_sorted_by_true, y)

        return loss
    
    
    
    
    # 5.2 数据准备
    originate_data_path="./data/GNN_data/"+repo_name+"/"
    data = GraphData(originate_data_path).data   #感觉是通用处理结点的方法，应该不需要改动
    '''
    return Data(x=x, 
            y=y, 
            adjacency_dict=adjacency_dict,
            train_mask=train_mask, 
            test_mask=test_mask)
    '''
    x=data.x
    adjacency_dict=data.adjacency_dict
    for i in range(len(x)):   #处理缺失数据或者规范化数据格式
        for j in range(len(x[0])):
            if np.isnan(x[i][j]): #如果x[i][j]是NaN值，则将其替换为0
                x[i][j]=0


    # 计算优先级标签
    label=[]
    y=data.y

    merge_result=[]
    life_cycle=[]
    # review_rounds=[]

    for i in range(len(y)):
        merge_result.append(y[i][0])
    for i in range(len(y)):
        life_cycle.append(y[i][1])
    # for i in range(len(y)):
    #     review_rounds.append(y[i][2])
    life_cycle.sort()  #根据响应速度排序
    # review_rounds.sort()     #根据关闭速度排序

    l=len(y)
    idx=[int(l/5),int(l*2/5),int(l*3/5),int(l*4/5)]
    

    threshold_life_cycle=[]  #存放四个值，按照int(l/5),int(l*2/5),int(l*3/5),int(l*4/5)划分的中间的值
    # threshold_review_rounds=[]
    for i in idx:
        threshold_life_cycle.append(life_cycle[i])
        # threshold_review_rounds.append(review_rounds[i])

    life_cycle_level=[]
    review_rounds_level=[]
    for i in y:   #确定响应速度等级，关闭速度等级
        if i[1]<threshold_life_cycle[0]:
            life_cycle_level.append(4)
        elif i[1]<threshold_life_cycle[1]:
            life_cycle_level.append(3)
        elif i[1]<threshold_life_cycle[2]:
            life_cycle_level.append(2)
        elif i[1]<threshold_life_cycle[3]:
            life_cycle_level.append(1)
        else:
            life_cycle_level.append(0)
        
        # if i[2]<threshold_review_rounds[0]:
        #     review_rounds_level.append(4)
        # elif i[2]<threshold_review_rounds[1]:
        #     review_rounds_level.append(3)
        # elif i[2]<threshold_review_rounds[2]:
        #     review_rounds_level.append(2)
        # elif i[2]<threshold_review_rounds[3]:
        #     review_rounds_level.append(1)
        # else:
        #     review_rounds_level.append(0)

    for i in range(len(life_cycle_level)):  #计算真实优先级，除以3
        # value=(merge_result[i]+life_cycle_level[i]+review_rounds_level[i])/3
        value=(merge_result[i]+life_cycle_level[i])/2
        label.append([value])

    label=np.array(label)  #转成array类型
    
    

    train_day_open_id,test_day_open_id=day_open_pr_id(repo_name)

#     count=0
#     total=0

#     for i in train_day_open_id:
#         count+=1
#         total+=len(i)
    
#     for i in test_day_open_id:
#         count+=1
#         total+=len(i)
    
#     print(total/count)

# train_process()


    train_data=[]
    tmp=[]

    for i in range(len(train_day_open_id)):
        for j in train_day_open_id[i]:
            tmp.append(j)
        if (i+1)%7==0:
            train_data.append(tmp)
            tmp=[]
    
    train_day_open_id=train_data
    #train_day_open_id的格式是一个列表，其中包含多个子列表，每个子列表代表一周的数据

    #   输出：  
    # Node's feature shape:  (2708, 1433)
    # Node's label shape:  (2708,)
    # Adjacency's shape:  2708
    # Number of training nodes:  140
    # Number of validation nodes:  500
    # Number of test nodes:  1000
    #   可以看到，数据集中共有2708个节点，节点特征有1433维，因此，GraphSAGE的输入维度INPUT_DIM = 1433。  
    # 5.3 模型初始化
    model_path = "./model/GNN_model/" + repo_name + "/"
    path_exists_or_create(model_path)
    INPUT_DIM = 75    # 输入维度  44-14
    # Note: 采样的邻居阶数需要与GCN的层数保持一致
    HIDDEN_DIM = [300,150,75]   # 隐藏单元节点数  #20,10,1  #10,10,1  10,10,1 10,10,1  10,10,5,1
    NUM_NEIGHBORS_LIST = [5,5,5]   # 每阶采样邻居的节点数 #5,5,5  #3,3,3 #3,2,2 2,2,2 3,3,3,3
    assert len(HIDDEN_DIM) == len(NUM_NEIGHBORS_LIST)
    BTACH_SIZE = 50     # 批处理大小
    EPOCHS = 5
    NUM_BATCH_PER_EPOCH = len(train_day_open_id)    # train里每个epoch循环的批次数
    NUM_BATCH_PER_EPOCH_TEST = len(test_day_open_id)    # test里每个epoch循环的批次数
    LEARNING_RATE = 0.01    # 学习率
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    print("【GNN/train.py】Device:", DEVICE)     # 他写的print(tf.config.list_physical_devices('GPU'))

    PATH=model_path+repo_name+'_model_state_dict_listwise'  #还有pairwise

    model = GraphSage(input_dim=INPUT_DIM, 
                      hidden_dim=HIDDEN_DIM,
                      num_neighbors_list=NUM_NEIGHBORS_LIST).to(DEVICE)
    print("【GNN/train.py】model=",model)
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=5e-4)


    def train(): #模型训练
        model.train() #将神经网络模型设为训练模式
        for e in range(EPOCHS): 
            for batch in range(NUM_BATCH_PER_EPOCH):
                #每个 epoch 包含 NUM_BATCH_PER_EPOCH 个 batch 的训练。
                
                #根据 batch_src_index 从 train_day_open_id 中获取源节点的索引，
                # 从 label 中获取该批次的标签，将其转换为 PyTorch 的张量并放到指定设备（如 GPU）上。
                batch_src_index=train_day_open_id[batch]
                batch_src_label = torch.from_numpy(label[batch_src_index]).float().to(DEVICE)
                #from_numpy()，它的作用是将一个 NumPy 数组转换成 PyTorch 中的 Tensor。
                #.float() 表示将该 Tensor 对象的数据类型设置为浮点型。
                
                batch_sampling_result = multihop_sampling(batch_src_index, NUM_NEIGHBORS_LIST, adjacency_dict,x)


                batch_sampling_x = [torch.from_numpy(x[idx]).float().to(DEVICE) for idx in batch_sampling_result]
                
                # 调用 multihop_sampling 函数对源节点进行多层采样，获取多个采样节点的索引，
                # 将每个采样节点的特征也转换为 PyTorch 的张量并放到指定设备上。

                batch_train_logits = model(batch_sampling_x)  
                #使用神经网络模型对采样节点进行预测，得到 batch_train_logits。



                #将标签和预测值分别转换为 Python 列表，打印输出以供调试。
                true_score=[]
                for i in range(len(batch_src_label)):
                    true_score.append(round(batch_src_label[i].cpu().numpy()[0],2))                
                print("【GNN/train.py】true_score:",true_score)
                pred_score=[]
                for i in range(len(batch_train_logits)):
                    pred_score.append(round(batch_train_logits[i].cpu().detach().numpy()[0],2))             
                print("【GNN/train.py】pred_score:",pred_score)


                optimizer.zero_grad()
                loss=listnet_loss(batch_src_label,batch_train_logits)
                #使用 ListNet 损失函数计算该 batch 的损失值，并进行反向传播和优化更新。
                # loss=pair_loss(batch_train_logits,batch_src_label)
                loss.backward()      
                optimizer.step()  # 使用优化方法进行梯度更新
                
        
            
            print("【GNN/train.py】epoch"+str(e+1)+"====================================================")
            test()
        

    def test():
        
        model.eval()  # 将GNN模型设为评估模式，即禁用Dropout和Batch Normalization等层
        with torch.no_grad():  #使用torch.no_grad()上下文管理器，以禁用自动求导功能，从而减少内存使用
            NDCG_L=[]
            MRR_L=[]
            KTD_L=[]
            for batch in range(NUM_BATCH_PER_EPOCH_TEST):
                
                #对于每个批次，将test_day_open_id中的相应索引赋值给batch_src_index，
                # 其中test_day_open_id是测试集数据的OpenID。
                batch_src_index=test_day_open_id[batch]
                # batch_src_index=train_index[start:end]
                
                #将batch_src_index对应的标签转换为张量类型，并移到指定设备上。
                batch_src_label = torch.from_numpy(label[batch_src_index]).float().to(DEVICE)

                #通过multihop_sampling函数从邻接字典中采样生成采样结果。
                batch_sampling_result = multihop_sampling(batch_src_index, NUM_NEIGHBORS_LIST, adjacency_dict,x)

                #将采样结果转换为张量类型，并移到指定设备上。
                batch_sampling_x = [torch.from_numpy(x[idx]).float().to(DEVICE) for idx in batch_sampling_result]
                
                #将batch_sampling_x作为输入传入模型，得到模型的预测结果batch_train_logits。
                batch_train_logits = model(batch_sampling_x)

                # 求ndcg
                dict_ground_truth=dict()

                batch_src_label=batch_src_label.cpu().numpy()
                for i,id in enumerate(batch_src_index):
                    dict_ground_truth[id]=batch_src_label[i]
                
                ground=[]
                for i in batch_src_label:
                    ground.append(i[0])
                ground.sort(reverse=True)

                            
                dict_pred=dict()
                for i,id in enumerate(batch_src_index):
                    dict_pred[id]=batch_train_logits[i]
                
                dict_pred_ranking=[]
                for id in sorted(dict_pred.items(), key=lambda item:item[1], reverse=True):
                    dict_pred_ranking.append(id[0])
                            
                pred_in_true_list=[]
                for i in dict_pred_ranking:
                    pred_in_true_list.append(dict_ground_truth[i][0])
                        
                p=len(batch_src_index)
                rel_true=ground
                rel_pred=pred_in_true_list
                
                ndcg_loss=NDCG(rel_true,rel_pred,p)
                mrr_loss=mrr(rel_true,rel_pred)
                ktd_loss=kendall_tau_distance(rel_true,rel_pred)

                # print(rel_pred)

                NDCG_L.append(ndcg_loss)
                MRR_L.append(mrr_loss)
                KTD_L.append(ktd_loss)        
            
            sum=0
            for item in NDCG_L:
                sum+=item
            Ndcg=sum/len(NDCG_L)
            sum=0
            for item in MRR_L:
                sum+=item
            Mrr=sum/len(MRR_L)
            sum=0
            for item in KTD_L:
                sum+=item
            Ktd=sum/len(KTD_L)

            print("【GNN/train.py】Test ndcg: ", Ndcg)
            print("【GNN/train.py】Test mrr: ", Mrr)
            print("【GNN/train.py】Test ktd: ", Ktd)
    train()
    torch.save(model.state_dict(), PATH+"_my.pt")    







