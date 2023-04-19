import getData
import sys
import os
sys.path.append(os.getcwd())
from util.path_exist import path_exists_or_create 

from repo_data import get_repo_name
repo_name=get_repo_name()


def build_filepath_edge():
    file_path_data=getData.getDataFromSql(
        "select pr_number,changed_file_name from\
        (select a.pr_number,changed_file_name,closed_at from \
        (select pr_number,changed_file_name  from  pr_file  where  repo_name='"+repo_name+"') as a, \
        (select pr_number,closed_at          from  pr_self  where  repo_name='"+repo_name+"') as b \
            where a.pr_number=b.pr_number) as c \
                where c.closed_at is not null "
    )

    ##字典保存pr修改的文件路径 （pr_number,文件路径）
    file_path_dict=[]
    file_path_dict.append((file_path_data[0][0],[file_path_data[0][1]]))  #[(1, [2])]这样的形式
    pr_number=file_path_data[0][0]
    file_path_dict=dict(file_path_dict)   
    #{1: [2]}  这样，pr_number便成为索引，file_path_dict[pr_number]为对应的文件路劲，文件路径由[]括起来


    for i in range(1,len(file_path_data)):
        if file_path_data[i][0]==pr_number:
            file_path_dict[pr_number].append(file_path_data[i][1])
        else:
            file_path_dict[file_path_data[i][0]]=[file_path_data[i][1]]
            pr_number=file_path_data[i][0]
    #上述过程，把pr_file中的数据抽取，形成dict ，file_path_dict[pr_number]里存放pr_number下所有路径的集合[road1,road2,road3]


    raw_data=getData.getDataFromSql(
        "select pr_number,created_at from pr_self where repo_name='"+repo_name+"'and closed_at is not null order by created_at asc"
    )
    #raw_data包含pr_number,created_at


    count=0
    process_data=[]
    for i in raw_data:
        process_data.append([i[0],count,i[1]])
        count+=1

    file_path = "./data/GNN_data/" + repo_name + "/"
    path_exists_or_create(file_path)

    f1 = open(file_path+repo_name+"_edge_filepath_source_my.txt",'w')
    f2 = open(file_path+repo_name+"_edge_filepath_destination_my.txt",'w')


    print("【build_filepath_edge】processing...")
    for i in process_data:
        if i[0] in file_path_dict.keys():# i[0] 为pr_number
            i_path=file_path_dict[i[0]]   #i[0](pr_number)对应的所有路径集合

            for j in process_data:
                if j[0] in file_path_dict.keys() and i[1]>j[1]:
                #j[0]为pr_number，i[1]>j[1]为count，为什么不用pr_number直接比？不知道
                    j_path=file_path_dict[j[0]] #j[0](pr_number)对应的所有路径集合
                    for k in i_path:
                        if k in j_path:
                            f1.writelines(str(i[1])+'\n')  #source      直接存的count，可能是想减小大小，按count算
                            f2.writelines(str(j[1])+'\n')  #destination
                            # break

    f1.close()
    f2.close()
    print("【build_filepath_edge】done!")

#如果修改的相同文件名越多，则重复的路径越多
#即i有road1，road2，road4
#j有road1，road4
#k有road4，road5
#则i指向j两次，指向k一次

# build_filepath_edge()




