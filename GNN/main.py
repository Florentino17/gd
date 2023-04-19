from nodes_Save import node_save
from build_filepath_edge import build_filepath_edge
from build_follow_edge import build_follow_edge
from my_01_node_save import my_01_node_save
from my_02_build_filepath_edge import my_02_build_filepath_edge
from my_04_edges_Save import my_04_edges_Save
from my_05_train import my_05_train_process
from my_06_eval import my_06_test_process
from edges_Save import edges_save
from train import train_process
from eval import test_process
import datetime

starttime = datetime.datetime.now()

my_01_node_save()
print("my_01_node_save")
my_02_build_filepath_edge()
print("my_02_build_filepath_edge")
my_04_edges_Save()
print("my_04_edges_Save")
my_05_train_process()
print("my_05_train_process")
my_06_test_process()
print("my_06_test_process")

# node_save() #保存结点
# print("【main】****************************node_save****************************")

# build_filepath_edge()  #构建文件路径_边
# print("【main】****************************build_filepath_edge****************************")

# build_follow_edge()   #构建关注_边
# print("【main】****************************build_follow_edge****************************")

# edges_save()        #保存边
# print("【main】****************************edges_save****************************")

# train_process()      #训练
# print("【main】****************************train_process****************************")

# test_process()      #测试
# print("【main】****************************test_process****************************")


endtime = datetime.datetime.now()
print("【main】时长：",end="")
print (endtime - starttime)  


