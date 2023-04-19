import sys
import os
sys.path.append(os.getcwd())
from repo_data import get_repo_name
repo_name=get_repo_name()
import getData
from util.path_exist import path_exists_or_create
from matplotlib import pyplot
import matplotlib.pyplot as plt
import pandas as pd

file_path = "./data/GNN_data"
path_exists_or_create(file_path)

repo_data=getData.getDataFromSql(
         "select date_format(created_at,'%Y-%m'),count(*) from pr_self where repo_name='"+repo_name+"' group by date_format(created_at,'%Y-%m')"
    )

# and closed_at is not null
# select DATE_FORMAT(createtime,'%Y-%m'),count(*) from test where user =8 group by DATE_FORMAT(createtime,'%Y-%m');//按月统计数据
# print(repo_data) 
# 
month=[]
num=[]   
for item in repo_data[:-24]:
    # print(item[0],item[1])
    month.append(str(item[0])[2:])
    num.append(item[1])


path=os.path.dirname(os.path.realpath(__file__))


# names = range(8,21)
names = month

x = range(len(month))
# y_train = [0.840,0.839,0.834,0.832,0.824,0.831,0.823,0.817,0.814,0.812,0.812,0.807,0.805]
# y_test  = [0.838,0.840,0.840,0.834,0.828,0.814,0.812,0.822,0.818,0.815,0.807,0.801,0.796]

plt.rcParams['font.sans-serif']=['SimHei']

plt.rcParams['axes.unicode_minus'] = False

plt.plot(x, num, marker='o', ms=3,label='GNN')
# plt.plot(x, RF[1:], marker='*', ms=3,label='Random Forest')
# plt.plot(x, XGB[1:], marker='^', ms=3,label='XGBoost')
# plt.plot(x, BN[1:], marker='s', ms=3,label='Bayes Network')
# plt.plot(x, FIFO[1:], marker='D', ms=3,label='FIFO')
# plt.plot(x, SJF[1:], marker='v', ms=3,label='SJF')
# plt.legend(loc='best',framealpha=0.3,markerscale=0.5,fontsize=5)  # 让图例生效


plt.xticks(x, names, rotation=1,fontsize=5)
plt.xticks(range(1,len(x),4),rotation=45)
plt.xticks(rotation=30) # 倾斜70度

plt.margins(0)
plt.subplots_adjust(bottom=0.10)
plt.xlabel('时间') #X轴标签
plt.ylabel("接收的PR数量") #Y轴标签
# pyplot.yticks([0.750,0.800,0.850])
pyplot.yticks([0,50,100,150,200,250,300,350,400,450,500,550,600,650])
# plt.title("PR优先级排序模型的结果统计") #标题
path=path+'\picture'
print("【pr_data_tendency】path=",path)
plt.savefig(path+'\\'+repo_name+'_pr_tendency_my.svg',format='svg',dpi = 10000)

# plt.savefig(path+'\\'+repo_name+'_pr_tendency_my.jpg',dpi = 10000)

