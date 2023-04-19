import sys
import os
sys.path.append(os.getcwd()) 
import torch
import csv
import numpy as np
from GraphSage import GraphSage
from GNN.data import GraphData
from sample import multihop_sampling
from day_split_data import day_open_pr_id
from eval_index.Kendall_tau_distance import kendall_tau_distance
from eval_index.mrr import mrr
from eval_index.ndcg import ndcg as NDCG
from repo_data import get_repo_name
from util.path_exist import path_exists_or_create
repo_name=get_repo_name()

def my_06_test_process():
    # 5.2 数据准备
    originate_data_path="./data/GNN_data/"+repo_name+"/"
    data = GraphData(originate_data_path).data
    x=data.x
    for i in range(len(x)):
        for j in range(len(x[0])):
            if np.isnan(x[i][j]):
                x[i][j]=0



# 计算优先级标签
    label=[]
    y=data.y
    merge_result=[]
    response_speed=[]
    # close_speed=[]
    for i in range(len(y)):
        merge_result.append(y[i][0])
    for i in range(len(y)):
        response_speed.append(y[i][1])
    # for i in range(len(y)):
    #     close_speed.append(y[i][2])
    response_speed.sort()
    # close_speed.sort()

    l=len(y)
    idx=[int(l/5),int(l*2/5),int(l*3/5),int(l*4/5)]

    threshold_response_speed=[]
    # threshold_close_speed=[]
    for i in idx:
        threshold_response_speed.append(response_speed[i])
        # threshold_close_speed.append(close_speed[i])

    response_speed_level=[]
    # close_speed_level=[]
    for i in y:
        if i[1]<threshold_response_speed[0]:
            response_speed_level.append(4)
        elif i[1]<threshold_response_speed[1]:
            response_speed_level.append(3)
        elif i[1]<threshold_response_speed[2]:
            response_speed_level.append(2)
        elif i[1]<threshold_response_speed[3]:
            response_speed_level.append(1)
        else:
            response_speed_level.append(0)
        
        # if i[2]<threshold_close_speed[0]:
        #     close_speed_level.append(4)
        # elif i[2]<threshold_close_speed[1]:
        #     close_speed_level.append(3)
        # elif i[2]<threshold_close_speed[2]:
        #     close_speed_level.append(2)
        # elif i[2]<threshold_close_speed[3]:
        #     close_speed_level.append(1)
        # else:
        #     close_speed_level.append(0)

    for i in range(len(response_speed_level)):
        # value=(merge_result[i]+response_speed_level[i]+close_speed_level[i])/3
        value=(merge_result[i]+response_speed_level[i])/2
        label.append([value])

    label=np.array(label)

    train_day_open_id,test_day_open_id=day_open_pr_id(repo_name)

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
    INPUT_DIM = 75    # 输入维度
    # Note: 采样的邻居阶数需要与GCN的层数保持一致
    HIDDEN_DIM = [300,150,75]   # 隐藏单元节点数
    NUM_NEIGHBORS_LIST = [5,5,5]   # 每阶采样邻居的节点数
    assert len(HIDDEN_DIM) == len(NUM_NEIGHBORS_LIST)
    BTACH_SIZE = 50     # 批处理大小
    EPOCHS = 1
    NUM_BATCH_PER_EPOCH = len(train_day_open_id)    # train里每个epoch循环的批次数
    LEARNING_RATE = 0.01    # 学习率
    NUM_BATCH_PER_EPOCH_TEST=len(test_day_open_id)
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    PATH=model_path+repo_name+'_model_state_dict_listwise_my.pt'
    # PATH=model_path+repo_name+'_model_state_dict_pairwise.pt'


    model = GraphSage(input_dim=INPUT_DIM, hidden_dim=HIDDEN_DIM,
                    num_neighbors_list=NUM_NEIGHBORS_LIST).to(DEVICE)
    print("【GNN/eval.py】model=",model)

    # model.load_state_dict(torch.load(PATH))
    model.load_state_dict(torch.load(PATH,map_location=torch.device('cpu')))
    # model.load_state_dict(torch.load(PATH),map_location=torch.device('cpu'))
    # model.load_state_dict(torch.load(PATH),_use_new_zipfile_serialization=False)


    def test():
        
        model.eval()
        with torch.no_grad():
            NDCG_L=[]
            MRR_L=[]
            KTD_L=[]
            for batch in range(NUM_BATCH_PER_EPOCH_TEST):
                
                batch_src_index=test_day_open_id[batch]
                # batch_src_index=train_index[start:end]
                
                batch_src_label = torch.from_numpy(label[batch_src_index]).float().to(DEVICE)
                batch_sampling_result = multihop_sampling(batch_src_index, NUM_NEIGHBORS_LIST, data.adjacency_dict,x)
                batch_sampling_x = [torch.from_numpy(x[idx]).float().to(DEVICE) for idx in batch_sampling_result]
                
                batch_train_logits = model(batch_sampling_x)
                pred_score=[]
                for i in range(len(batch_train_logits)):
                    pred_score.append((batch_src_index[i],batch_train_logits[i].cpu().numpy()[0]))

                print("【GNN/eval.py】pred_score",pred_score)

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

                sort_result=[]            
                pred_in_true_list=[]
                for i in dict_pred_ranking:
                    sort_result.append(i)
                    pred_in_true_list.append(dict_ground_truth[i][0])
                
                print("【GNN/eval.py】sort_result",sort_result)
                        
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

            row_data=[]
            print("【GNN/eval.py】Test ndcg: ", Ndcg)
            print("【GNN/eval.py】Test mrr: ", Mrr)
            print("【GNN/eval.py】Test ktd: ", Ktd)

            row_data.append([Ndcg,Mrr,Ktd])
            # row_data.append(Mrr)
            # row_data.append(Ktd)

            headers = [
                'ndcg_mean',
                'mrr_mean',
                'kendall_tau_distance_mean'
                ]

            result_path = "./result/GNN/"
            path_exists_or_create(result_path)
            with open(result_path + repo_name+"_result_pairwise_my.csv",
                'w+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, dialect='excel')
                writer.writerow(headers)
                for item in row_data:
                    writer.writerow(item)
    test()





