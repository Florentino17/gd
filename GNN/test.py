from re import sub
from urllib.request import HTTPBasicAuthHandler
import getData
import sys
import os
sys.path.append(os.getcwd())
from util.path_exist import path_exists_or_create 

from repo_data import get_repo_name
repo_name=get_repo_name()


import torch
 


# true=[3,2,1,3,5]
# # pre=[1,2,3,4,5]
# pre=[3,2,1,3,5]

# loss=list_mle(torch.tensor(pre),torch.tensor(true),k=3)
# print(loss)
d={0:1.3,1:2.3}
print("【GNN/test.py】d=",d)





