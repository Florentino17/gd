import getData
import sys
import os
sys.path.append(os.getcwd())
from util.path_exist import path_exists_or_create 

from repo_data import get_repo_name
repo_name=get_repo_name()

def build_follow_edge():
    #从数据库获取user信息
    raw_data=getData.getDataFromSql(
        "select user_id,followers,following from pr_user"
    )

    dict_follower=[]
    dict_following=[]

    for item in raw_data:
        ##follower  关注他的
        tmp=[]
        
        for i in eval(item[1]).split(';'):
            print("【build_follow_edge】i==",i)
            id=i.split('-')[0]
            print("【build_follow_edge】id==",id)
            if id!='':
                tmp.append(int(id))
        dict_follower.append((item[0],tmp))
        ##following  他关注的
        tmp=[]
        for i in eval(item[2]).split(';'):
            id=i.split('-')[0]  #用-隔开，并取前一部分，，，str(114660397)
            if id!='':
                tmp.append(int(id))         #int(114660397)
        dict_following.append((item[0],tmp))  # user_id,  int(114660397)用户id集合

        # print("\n\n")
        # print("eval(item[1]).split(';')==",eval(item[1]).split(';'))
        # print("\n\n")
        # print("type(item[1])=",type(item[1]))
        # print("\n\n")
        # print("item[1]=",item[1])
        # print("\n\n")
        # print("eval(item[1])=",eval(item[1]))
        # print("\n\n")
    '''
    item[1]= "4401-wuwx;15062-Grauwolf;23088-robbyoconnor;23809-resmo;"和数据库中一样
    type(item[1])= <class 'str'>
    eval(item[1])= 4401-wuwx;15062-Grauwolf;23088-robbyoconnor;23809-resmo; #eval函数把双引号去除
    eval(item[1]).split(';')== ['4401-wuwx', '15062-Grauwolf', '23088-robbyoconnor', '23809-resmo','']
    i== 114660397-IceCYow
    id== 114660397
    '''


    ##user的follower和following
    dict_follower=dict(dict_follower)
    dict_following=dict(dict_following)

    user_path_data=getData.getDataFromSql(
        "select pr_user_id,created_at from pr_self where repo_name='"+repo_name+"'and closed_at is not null order by created_at asc"
    )

    ##打pr_id
    process_data=[]
    count=0
    for item in user_path_data:
        process_data.append([item[0],count,item[1]])
        count+=1
    
    user_pr_dict={}

    # 保存(user_id,[pr_id_list])
    for item in process_data:
        if item[0] in user_pr_dict.keys():
            user_pr_dict[item[0]].append([item[1],item[2]])
        else:
            user_pr_dict[item[0]]=[]
            user_pr_dict[item[0]].append([item[1],item[2]])
    
    # 找到该项目PR中所有的用户
    user_total=[]
    for item in user_pr_dict.keys():
        user_total.append(item)
    
    follow={}
    following={}
    for item in user_total:
        if item in dict_follower.keys():
            follow[item]=dict_follower[item]
            following[item]=dict_following[item]


    print("【build_follow_edge】processing...")

    file_path = "./data/GNN_data/" + repo_name + "/"
    path_exists_or_create(file_path)

    f1 = open(file_path+repo_name+"_edge_follow_source_my.txt",'w')
    f2 = open(file_path+repo_name+"_edge_follow_destination_my.txt",'w')

    # 遍历该项目PR中所有的用户
    for item in follow.keys():
        # 取出该用户提交的所有PR_id和日期
        temp_pr_1=user_pr_dict[item]
        # 取出该用户关注的所有用户
        for i in follow[item]:
            # 如果关注的用户也在该项目中出现
            if i in user_total:
                if i in follow.keys() and item in follow[i]:
                    # 取出关注的用户提交的所有PR_id
                    temp_pr_2=user_pr_dict[i]
                    for j in temp_pr_1:
                        for k in temp_pr_2:
                            if j[0]>k[0]:
                            # if j[0]>k[0]:
                                f1.write(str(j[0])+'\n')
                                f2.write(str(k[0])+'\n')
                                
        

    for item in following.keys():
        temp_pr_1=user_pr_dict[item]
        for i in following[item]:
            if i in user_total:
                if i in following.keys() and item in following[i]:
                    temp_pr_2=user_pr_dict[i]
                    for j in temp_pr_1:
                        for k in temp_pr_2:
                            if j[0]>k[0]:
                            # if j[0]>k[0]:
                                f1.write(str(j[0])+'\n')
                                f2.write(str(k[0])+'\n')
                

    

    ##构边并保存

    print("【build_follow_edge】done!")