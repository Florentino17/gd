import sys
import os
sys.path.append(os.getcwd())
import getData
import numpy as np
from util.date_utils.date_function import is_weekday_commit\
    ,project_age,get_waiting_time,get_close_pr_time
from util.num_utils.num_function import get_label_count\
    ,get_workload,get_prev_prs,get_change_num\
    ,get_accept_num,get_close_num,get_review_num\
    ,get_participants_count
from util.str_utils.str_function import wordCount
from util.num_utils.num_ratio_function import get_pr_author_rate\
    ,get_project_line_rate,get_line_weekday_rate,get_project_line_churn_rate\
        ,get_commits_average,get_avg_comments,get_avg_latency
from util.path_exist import path_exists_or_create

basedir = os.path.abspath(os.path.dirname(__file__))
from repo_data import get_repo_name
repo_name=get_repo_name()

def my_01_node_save():
    raw_data=getData.getDataFromSql(
        "select * from pr_all  where pid<=1000 order by created asc"
    )
    
    print("【node_save】len(raw_data)=",len(raw_data))##查看PR数量
    # print(raw_data[1][2])
    row_num=(int)(np.size(raw_data)/len(raw_data))
    print("num of column=",row_num)

    useful_features_index=[]
    # useful_features_index.append(2)
    for i in range(5,row_num-5):
        useful_features_index.append(i)
    
    selected_data=[]
    for item in raw_data:
        tmp=[]
        for i in useful_features_index:
            tmp.append(item[i])
        selected_data.append(tmp)
    print(len(selected_data))


    X_successive=selected_data
    X_successive=np.array(X_successive)
    mins = X_successive.min(0) #返回data矩阵中每一列中最小的元素，返回一个列表
    maxs = X_successive.max(0) #返回data矩阵中每一列中最大的元素，返回一个列表
    ranges = maxs - mins #最大值列表 - 最小值列表 = 差值列表
    normData = np.zeros(np.shape(X_successive)) #生成一个与 data矩阵同规格的normData全0矩阵，用于装归一化后的数据
    row = X_successive.shape[0] #返回 data矩阵的行数
    normData = X_successive - np.tile(mins,(row,1)) #data矩阵每一列数据都减去每一列的最小值
    normData = normData / np.tile(ranges,(row,1))
    X_successive=normData.tolist()

    X=X_successive
    headers=['Id',
        #project
        # 'change_id' ,
       # created , 
       # subject ,
        'author_experience' , 

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
        'avg_score',
        #'user_id'

        #'close',
        'status' ,
        'time' ,
        'rounds' 
            ]
    
    ##是否被合并  (70%)
    Y_1=[]
    for i in range(0,len(raw_data)):
        Y_1.append(int(raw_data[i][row_num-3])*4)
    
    # 关闭速度
    Y_2=[]
    for i in range(0,len(raw_data)):
        Y_2.append((float)(raw_data[i][row_num-2]))
    
    # # 评审轮数
    # Y_3=[]
    # for i in range(0,len(raw_data)):
    #     Y_3.append((int)(raw_data[i][row_num-1]))

    Y=[]
    for i in range(0,len(Y_1)):
        Y.append([Y_1[i],Y_2[i]])

    row_data=[]
    count=0
    for i in range(len(X)):
        tmp=[]
        tmp.append(count)
        count+=1
        for x in X[i]:
            tmp.append(x)
        for x in Y[i]:
            tmp.append(x)
        row_data.append(tmp)
    # 保存数据到csv文件
    import csv
    file_path = "./data/GNN_data/" + repo_name + "/"
    path_exists_or_create(file_path)

    with open(file_path+'nodes_data_'+repo_name+'my.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(headers)
        for item in row_data:
            writer.writerow(item)
    return 
my_01_node_save()


