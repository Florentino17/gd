import getData
import os

basedir = os.path.abspath(os.path.dirname(__file__))




def day_open_pr_id(repo_name):

    # 按PR到来时间读取by created_at asc
    time_data=getData.getDataFromSql(
        "select created,closed from pr_all where pid<=1000 order by created asc"
    )  # 读取的内容是created_at,closed_at

    print("【GNN/day_split_data.py】type(time_data)=",type(time_data))   #输出time_data数据类型
    print("【GNN/day_split_data.py】time_data=",time_data)   #输出time_data

    # 按8:2划分训练集和数据集，并获取分界点的日期
    print("【GNN/day_split_data.py】time_data[int(len(time_data)*0.8)][0]=",
          time_data[int(len(time_data)*0.8)][0])   #[0]即created_at,[1]是closed_at，位于80%位置的即created_at时间
    print("【GNN/day_split_data.py】type(time_data[int(len(time_data)*0.8)][0])=",
          type(time_data[int(len(time_data)*0.8)][0])) #输出这个的类型
    train_test_threshold=time_data[int(len(time_data)*0.8)][0].date()  #还是这个时间，转换为date类型
    print("【GNN/day_split_data.py】train_test_threshold=",train_test_threshold) #输出这个分割时间
    # train_test_threshold=time_data[int(len(time_data)*0.8)][0]
    # 划分训练集数据集
    train_day=[]
    test_day=[]

    day_data={}
    create_time_index=0
    close_time_index=1
    
    # 按PR到来日期生成字典
    for id,i in enumerate(time_data):
        create_day=i[0].date()  # create_day是一个日期对象，表示PR的创建日期
        # create_day=i[0]
        if day_data.__contains__(create_day):
            day_data[create_day][id]={}
            day_data[create_day][id]['create_time']=i[create_time_index]
            day_data[create_day][id]['close_time']=i[close_time_index]
        else:
            day_data[create_day]={}
            day_data[create_day][id]={}
            day_data[create_day][id]['create_time']=i[create_time_index]
            day_data[create_day][id]['close_time']=i[close_time_index]


    # 对于每个PR到来日，更新列表中还未关闭的PR
    for day in day_data.keys():  #keys可能是create_day
        tmp=[]
        if day<=train_test_threshold:   #前80%
            for key in day_data.keys():
                if key>day:
                    continue
                else:                #小于day的
                    temp_pr_dict=day_data[key]  #小于day的这个数据
                    for pr_id in temp_pr_dict:  #找到这天所有pr
                        if temp_pr_dict[pr_id]['close_time'].date()<day: #还没关闭的pr
                            continue
                        else:
                            tmp.append(pr_id)  #加入tmp
            if len(tmp)>0:
                train_day.append(tmp) #加入train_day
        
        else:                           #后20%
            for key in day_data.keys():
                if key>day:
                    continue
                else:           #找小于day的
                    temp_pr_dict=day_data[key]
                    for pr_id in temp_pr_dict:
                        if temp_pr_dict[pr_id]['close_time'].date()<day:
                            continue
                        else:
                            tmp.append(pr_id)
            if len(tmp)>0:
                test_day.append(tmp)     #上面类似，这里加入test_day

    return train_day,test_day


