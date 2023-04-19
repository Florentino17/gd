# 读取数据
import pandas as pd
import datetime
import numpy as np
import pymysql
import pandas as pd
import math
import json
# data = pd.read_csv("E://Desktop//data//Eclipse.csv")
# data = pd.read_csv("E://Desktop//data//data_eclipse.csv")
data = pd.read_csv("E://Desktop//data//data_eclipse_1.csv")

row_num=data.shape[0]
line_num=data.shape[1]
print("row_num line_num ",row_num,line_num)


def connect_to_database():
    db=pymysql.connect(host='localhost',user='root',password='123456',charset='utf8',db="gd_eclipse")
    cursor=db.cursor()
    return db,cursor

def shijian(dd):
    dd = datetime.datetime.strptime(dd, "%Y-%m-%d %H:%M:%S")
    return dd

def my_is_nan(mynan):
    return mynan != mynan




def data_process():
    for i in range(0,row_num):
        data.iloc[i,2]=shijian(data.iloc[i,2].split('.')[0])
        # print(type(data.iloc[i,2]))
        if (i%5000==0):
            print(i,"date")
            # break
    print("created_date--end")

    closed=[]
    for i in range(0,row_num):
        day_length=data.iloc[i,line_num-2]
        closed_date=data.iloc[i,2]+datetime.timedelta(days=day_length)
        closed.append(closed_date)
        if (i%5000==0):
            print(i,"close_date",data.iloc[i,2],closed_date,data.iloc[i,line_num-2])

    data.insert(loc=line_num-3, column='closed', value=closed)
    print("closed_date--end")

    

    for i in range(0,line_num):
        tp=str(data.iloc[0,i])
        # print(tp)
        # print(type(tp))
        if tp=="True" or tp=="False":
            # print(1)
            for j in range(0,row_num):
                data.iloc[j,i]=(int)(data.iloc[j,i])
            # print(data.columns[i])
                if (j%5000==0):
                    print(j,data.columns[i])

    data.to_csv("E://Desktop//data//data_eclipse.csv",index=False)
def write_to_database():
    db,cursor=connect_to_database()

    try:
    #1
        #85个属性，id+84个
        insert_sql='''
        insert into pr_all values(\
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
            %s,%s,%s,%s,%s)
        '''

        print(111111)
        start_num=4320
        for i in range(start_num,row_num):
            idx=i+1
            # cursor.execute(insert_sql)
            d=[]
            for j in range(0,line_num):
                tp=data.iloc[i,j]
                if my_is_nan(tp):
                    tp="Nothing"
                # print(tp)
                d.append(tp)
            # print(d)
            values=(idx,\
                    d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],\
                    d[10],d[11],d[12],d[13],d[14],d[15],d[16],d[17],d[18],d[19],\
                    d[20],d[21],d[22],d[23],d[24],d[25],d[26],d[27],d[28],d[29],\
                    d[30],d[31],d[32],d[33],d[34],d[35],d[36],d[37],d[38],d[39],\
                    d[40],d[41],d[42],d[43],d[44],d[45],d[46],d[47],d[48],d[49],\
                    d[50],d[51],d[52],d[53],d[54],d[55],d[56],d[57],d[58],d[59],\
                    d[60],d[61],d[62],d[63],d[64],d[65],d[66],d[67],d[68],d[69],\
                    d[70],d[71],d[72],d[73],d[74],d[75],d[76],d[77],d[78],d[79],\
                    d[80],d[81],d[82],d[83])
            
            cursor.execute(insert_sql, values)
            #将数据提交给数据库（加入数据，修改数据要先提交）
            db.commit()
            if (i%1000==0):
                print(i,"insert")
    except Exception as e:
        print(e)

    #无论是否报错都执行
    finally:
        cursor.close()
        db.close() 
def test():
    for i in range(0,row_num):
        data.iloc[i,2]=shijian(data.iloc[i,2].split('.')[0])
        # print(type(data.iloc[i,2]))
        if (i%5000==0):
            print(i,"date")
            c=(data.iloc[i,2]+datetime.timedelta(days=123))
            print(data.iloc[i,2])
            print(c)
    
    print("date--end")
    pass
def extract_user():
    # #"E:\Desktop\data\Eclipse\changes"
    # # 数据路径
    # path = "E://Desktop//data//Eclipse//changes//Eclipse_108_change.json"
    # # 读取文件数据
    # with open(path, "r") as f:
    #     row_data = json.load(f)
    # # 读取每一条json数据
    # user_id=(int)(row_data["owner"]["_account_id"])
    # print(type(user_id))
    # # for d in row_data:
    # #     print(d)
    user_id_list=[]
    print(len(user_id_list))
    for i in range(0,row_num):
        changed_id=data.iloc[i,1]
        path = "E://Desktop//data//Eclipse//changes//Eclipse_"+(str)(changed_id)+"_change.json"
        with open(path, "r") as f:
            row_data = json.load(f)
        # 读取每一条json数据
        user_id=(int)(row_data["owner"]["_account_id"])
        user_id_list.append(user_id)
        # print(path,user_id)
        # print(changed_id)
        # if i>50:
        #     break
        if i%1000==0:
            print(i,"user_id")
    print(len(user_id_list))
    data.insert(loc=line_num-3, column='user_id', value=user_id_list)
    data.to_csv("E://Desktop//data//data_eclipse_1.csv",index=False)
    pass
def extract_filename():

    id_list=[]
    file_list=[]
    # sum_file=0
    
    sum_file=0

    last_i=-1
    set_file=set()
    for i in range(0,1050): #for i in range(0,row_num):
        changed_id=data.iloc[i,1]
        path = "E://Desktop//data//Eclipse//changes//Eclipse_"+(str)(changed_id)+"_change.json"
        with open(path, "r") as f:
            row_data = json.load(f)
        filename_set=row_data["revisions"]  #da294165aa8e635f56cf379e3e064ca9318f09be集合
        for filename in filename_set:
            str_filename=(str)(filename)
            for file in row_data["revisions"][str_filename]["files"]: 
                # print(i,file)
                if i!=last_i:  #去重
                    last_i=i
                    set_file=set()
                if file not in set_file:
                    set_file.add(file)
                    id_list.append(i+1)
                    file_list.append(file)
                    sum_file+=1

    print(set_file)
    print(sum_file)
    start_num=1
    db,cursor=connect_to_database()

    try:
    #1
        #85个属性，id+84个
        insert_sql='''
        insert into pr_all_file values(%s,%s,%s)
        '''

        print(111111)
        start_num=1
        for i in range(0,sum_file):
            
            values=(start_num+i,id_list[i],file_list[i])
            
            cursor.execute(insert_sql, values)
            #将数据提交给数据库（加入数据，修改数据要先提交）
            db.commit()
            if (i%1000==0):
                print(i,"insert")
    except Exception as e:
        print(e)

    #无论是否报错都执行
    finally:
        cursor.close()
        db.close() 

        # if i>10:
        #     break
    # path = "E://Desktop//data//Eclipse//changes//Eclipse_108_change.json"
    # with open(path, "r") as f:
    #     row_data = json.load(f)
    # # 读取每一条json数据
    # for d in row_data:
    #     print(d)
    # print()
    # filename=row_data["revisions"]
    # # print(filename)
    # for c in filename:
    #     print(c)
    # print(row_data["revisions"]["da294165aa8e635f56cf379e3e064ca9318f09be"]["files"])
    # for file in row_data["revisions"]["da294165aa8e635f56cf379e3e064ca9318f09be"]["files"]:
    #     print(file)
    pass

if __name__== "__main__" :
    # data_process()
    # extract_user()
    extract_filename()
    # write_to_database()
    pass




