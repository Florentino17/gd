# from cv2 import merge
import pymysql as db
import requests
import time
import json
import sys 
import os



# abs_path=os.path.abspath(__file__).split("\\")
# upper_level_dic="\\".join(abs_path[:-2])
# sys.path.append("d:\Code\Python\GNN\week30")


# abs_path=os.path.abspath(__file__).split("\\")
# upper_level_dic="\\".join(abs_path[:-2])
# sys.path.append("d:\Code\Python\GNN\week30")


sys.path.append(os.getcwd())
from util.access_token import get_token
# get_token()

# repo_r = requests.get("https://api.github.com/repos/activemerchant/active_merchant", 
#                     headers={'Authorization': 'token ' + get_token()})
 
# print(repo_r.json())

merged=12
re=((merged == True) and 1 or 0)

print(re)