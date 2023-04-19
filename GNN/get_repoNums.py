import sys
import os
from unittest import result

from sympy import re
sys.path.append(os.getcwd())
from repo_data import get_repo_name
repo_name=get_repo_name()
import getData
from util.path_exist import path_exists_or_create
import csv

file_path = "./data/GNN_data/repo_Nums"
path_exists_or_create(file_path)

repo_data=getData.getDataFromSql(
        "select repo_name from pr_repo"
    )

# repo_data=repo_data[:3]


repo_dict={}

for name in repo_data:
    print("【get_repoNums】name[0]=",name[0])
    repo_nums=getData.getDataFromSql(
        "select count(*) from pr_self where repo_name='"+name[0]+"'"
    )
    repo_dict[name[0]]=repo_nums[0][0]

result=sorted(repo_dict.items(),key=lambda d:d[1])


re=[]

for item in result:
    tmp=[]
    merge_num=getData.getDataFromSql(
        "select count(*) from pr_self where repo_name='"+item[0]+"' and merged_at is not null"
    )
    merge_ratio=merge_num[0][0]/item[1]
    tmp.append(item[0])
    tmp.append(item[1])
    tmp.append(merge_ratio)
    re.append(tmp)
    


headers=['repo','pr_nums','merge_ratio']

with open(file_path+'.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, dialect='excel')
    writer.writerow(headers)
    for item in re:
        writer.writerow(item)


