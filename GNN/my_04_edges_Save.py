import sys
import os
sys.path.append(os.getcwd()) 
import getData
import csv
import numpy as np
from repo_data import get_repo_name
repo_name=get_repo_name()
from util.path_exist import path_exists_or_create


def my_04_edges_Save():
    #从数据库获取数据
    raw_data=getData.getDataFromSql(
        "select * from pr_all where pid<=1000 order by created asc"
    )
    print("【edges_Save】=",len(raw_data))##查看PR数量

    row_num=(int)(np.size(raw_data)/len(raw_data))
    print("num of column=",row_num)
    useful_features_index=[0,row_num-4]

    selected_data=[]
    for item in raw_data:
        tmp=[]
        for i in useful_features_index:
            tmp.append(item[i])
        selected_data.append(tmp)
    print(len(selected_data))
    # useful_features_index=[1,##pr_number
    #     3,##repo_name
    #     4,##pr_user_id
    #     6,##pr_author_association
    #     9,##labels
    #     11,##created_at
    #     13,##closed_at
    #     14,##merged_at
    #     15,##merged
    #     17,##mergeable_state
    #     19,##assignees_content
    #     21,##comments_number
    #     22,##comments_content
    #     23,##review_comments_number
    #     24,##review_comments_content
    #     25,##commit_number
    #     27,##changed_file_num
    #     28,##total_add_line
    #     29,##total_delete_line
    #     5,##pr_user_name
    #     12,##updated_at
    #     7,##title
    #     8,##body
    #     ]



    # selected_data=[] ##保留有用的属性特征
    # for item in raw_data:
    #     tmp=[]
    #     for i in useful_features_index:
    #         tmp.append(item[i])
    #     selected_data.append(tmp)



    # process_data=[]
    # count=0
    # for item in selected_data:
    #     tmp=[]
    #     ##pr_number
    #     tmp.append(item[0])
    #     ##repo_name
    #     tmp.append(item[1])
    #     ##pr_user_id
    #     tmp.append(item[2])
    #     ####pr_author_association
    #     if item[3]=='CONTRIBUTOR':
    #         tmp.append(0)
    #     elif item[3]=='MEMBER':
    #         tmp.append(1)
    #     elif item[3]=='NONE':
    #         tmp.append(2)
    #     else:
    #         tmp.append(3)

    #     ##labels
    #     if item[4]=='{}':
    #         tmp.append(0)
    #     else:
    #         tmp.append(1)
        
    #     ##created_at
    #     tmp.append(item[5])
    #     ##closed_at
    #     tmp.append(item[6])
    #     ##merged_at
    #     tmp.append(item[7])

    #     ##merged
    #     tmp.append(item[8])

    #     ##mergeable_state
    #     if item[9]=='unknown':
    #         tmp.append(0)
    #     elif item[9]=='blocked':
    #         tmp.append(1)
    #     elif item[9]=='dirty':
    #         tmp.append(2)
    #     else:
    #         tmp.append(3)

    #     ##assignees_content
    #     if item[10]=='{}':
    #         tmp.append(0)
    #     else:
    #         tmp.append(1)

    #     ##comments_number
    #     tmp.append(item[11])
        
    #     ##comments_content
    #     tmp.append(item[12])
    #     ##review_comments_number
    #     tmp.append(item[13])
    #     ##review_comments_content
    #     tmp.append(item[14])
    #     ##commit_number
    #     tmp.append(item[15])
    #     ##changed_file_num
    #     tmp.append(item[16])
    #     ##total_add_line
    #     tmp.append(item[17])
    #     ##total_delete_line
    #     tmp.append(item[18])

    #     ##pr_username
    #     tmp.append(item[19])

    #     ##pr_id
    #     tmp.append(count)

    #     ##updated_at
    #     tmp.append(item[20])
        
    #     ##content
    #     tmp.append(item[4])

    #     ##title
    #     tmp.append(item[21])

    #     ##body
    #     tmp.append(item[22])

    #     count+=1
    #     process_data.append(tmp)


    ###构造3种边
    edge_source=[]
    edge_target=[]


    pr_user_id_index=2
    pr_id_index=20
    created_index=5

    author_edge={}

###################################################################################

    pr_id_index=0
    pr_user_id_index=1
    

    ####### 1.相同提交者的PR之间有边：
    for i in selected_data:
        for j in selected_data:
            if i[pr_user_id_index]==j[pr_user_id_index] and i[pr_id_index]>j[pr_id_index]: #pr_user_id_index=2
                # print(i[pr_user_id_index],i[pr_id_index],j[pr_id_index])
                edge_source.append(i[pr_id_index]-1)
                edge_target.append(j[pr_id_index]-1)

    file_path = "./data/GNN_data/" + repo_name + "/"
    path_exists_or_create(file_path)

    ####### 2.修改文件路径相同的有边：
    f = open(file_path+repo_name+"_edge_filepath_source_my.txt")
    data = f.readlines()
    f.close()
    for i in data:
        edge_source.append(int(i.strip('\n')))  #这里的i是每一行的数据+\n,去处\n，int即把str变为int，
    

    f = open(file_path+repo_name+"_edge_filepath_destination_my.txt")  
    data = f.readlines()
    f.close()
    for i in data:
        edge_target.append(int(i.strip('\n')))   #上面是edge_source，这里是添加到edge_target

    # ####### 3.PR作者间关系是follow或者被follow的有边：

    # f = open(file_path+repo_name+"_edge_follow_source_my.txt")
    # data = f.readlines()
    # f.close()
    # for i in data:
    #     edge_source.append(int(i.strip('\n')))  #edge_source
    

    # f = open(file_path+repo_name+"_edge_follow_destination_my.txt")
    # data = f.readlines()
    # f.close()
    # for i in data:
    #     edge_target.append(int(i.strip('\n')))  #edge_target

    ######## 保存数据到csv文件

    headers=['SrcId','DesId','Weight']

    row_data=[]

    for i in range(len(edge_source)):
        tmp=[]
        tmp.append(edge_source[i])
        tmp.append(edge_target[i])
        tmp.append(1)
        row_data.append(tmp)
            

    ######## 保存数据到csv文件
    with open(file_path+'edges_data_'+repo_name+'my.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(headers)
        for item in row_data:
            writer.writerow(item)


my_04_edges_Save()




