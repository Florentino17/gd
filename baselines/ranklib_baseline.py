'''
获取到所有的PR信息，找出每一个PR创建的时间，以及在该PR创建时间那个时刻仍处于open状态的pr，
然后将这个时刻还处于open状态的pr作为输入X。
FIFO算法，根据pr创建的时间先创建，放在最前面，这样对上述pr列表进行排序。FIFOY
真实排序：在该时刻之后，该X中，被相应，或者被关闭或者被合并等发生改变的时间，根据该时间顺序进行排序，进而获取真实排序TRUEY
将FIFOY，与TRUEY进行比较，通过NDcg进行比较，判断排序效果
'''
import sys
import os
sys.path.append(os.getcwd()) 
import data_processing.get_data_from_database.database_connection as dbConnection
from baselines.true_order import get_true_order_dict
from eval_index.Kendall_tau_distance import kendall_tau_distance
from eval_index.mrr import mrr
from util.date_utils.date_function import  get_close_pr_time,get_waiting_time
import csv
from eval_index.ndcg import ndcg
# Python的标准库linecache模块非常适合这个任务
import os
from util.path_exist import path_exists_or_create
from GNN.repo_data import get_repo_name
# 增加代码的可读性
pr_number_index = 0
repo_name_index = 1
pr_user_id_index = 2
pr_user_name_index = 3
pr_author_association_index = 4
labels_index = 5
created_at_index = 6
closed_at_index = 7
merged_at_index = 8
updated_at_index = 9
merged_index = 10
mergeable_state_index = 11
assignees_content_index = 12
comments_number_index = 13
comments_content_index = 14
review_comments_number_index = 15
review_comments_content_index = 16
commit_number_index = 17
changed_file_num_index = 18
total_add_line_index = 19
total_delete_line_index = 20
title_index = 21
body_index = 22


# 根据所在原始文件中pr_number获取当前测试需要的文件
# 获取当前文件中pr——number，以及对应的索引位置
def get_pr_number_from_origin_data_path(origin_data_path):
    file_pr_dict = {}
    count = 0
    for line in open(origin_data_path):
        line_str = line.partition("# ")
        # 找到pr_number对应的索引位置
        file_pr_dict[int(line_str[2])] = count
        count = count + 1
    return file_pr_dict # {pr_number:index}


def get_data_by_repo_name_and_origin_data_path(origin_data_path, repo_name):
    data = dbConnection.getDataFromSql(
        "select * from pr_self where repo_name='" + repo_name + "' and closed_at is not null order by pr_number")

    print("【ranklib_baseline.py】len(data)=",len(data))  ##查看PR数量
    # 获取所在文件中的prlist
    file_pr_dict = get_pr_number_from_origin_data_path(origin_data_path)
    # 标记有用的PR自身信息的下标
    useful_features_index = [0,  ##pr_number
                             2,  ##repo_name
                             3,  ##pr_user_id
                             4,  ##pr_user_name
                             5,  ##pr_author_association
                             8,  ##labels
                             10,  ##created_at
                             12,  ##closed_at
                             13,  ##merged_at
                             11,  ##updated_at
                             14,  ##merged
                             16,  ##mergeable_state
                             18,  ##assignees_content
                             20,  ##comments_number
                             21,  ##comments_content
                             22,  ##review_comments_number
                             23,  ##review_comments_content
                             24,  ##commit_number
                             26,  ##changed_file_num
                             27,  ##total_add_line
                             28,  ##total_delete_line
                             6,  ##title
                             7,  ##body
                             ]
    #######################修改数据库后的定义                     
    for i in range(0,len(useful_features_index)):
        useful_features_index[i]+=1

    ##保留有用的属性特征
    selected_data = []
    for item in data:
        tmp = []
        for i in useful_features_index:
            tmp.append(item[i])
        selected_data.append(tmp)
    pr_time = []
    merge_result_dict={}
    day_data = {}
    for item in selected_data:
        tmp = []
        created_time = item[created_at_index]
        created_day = created_time.date()
        if day_data.__contains__(created_day):
            day_data[created_day][item[pr_number_index]] = {}
            day_data[created_day][item[pr_number_index]]['created_time'] = item[created_at_index]
            day_data[created_day][item[pr_number_index]]['closed_time'] = item[closed_at_index]
        else:
            day_data[created_day] = {}
            day_data[created_day][item[pr_number_index]] = {}
            day_data[created_day][item[pr_number_index]]['created_time'] = item[created_at_index]
            day_data[created_day][item[pr_number_index]]['closed_time'] = item[closed_at_index]
        tmp.append(('created_time', item[created_at_index]))
        tmp.append(('updated_time', item[updated_at_index]))
        tmp.append(('closed_time', item[closed_at_index]))
        tmp.append(('comments_number', item[comments_number_index]))
        tmp.append(('comments_content', item[comments_content_index]))
        tmp.append(('review_comments_number', item[review_comments_number_index]))
        tmp.append(('review_comments_content', item[review_comments_content_index]))
        tmp.append(('pr_user_name', item[pr_user_name_index]))
        tmp = dict(tmp)
        pr_time.append((item[pr_number_index], tmp))
        merge_result_dict[item[pr_number_index]] = int(item[merged_index])*4

       
    pr_time = dict(pr_time)
    first_response_time_dict = get_waiting_time(pr_time)
    close_time_dict = get_close_pr_time(pr_time)
    # print(first_response_time_dict)
    # 响应时间 按照pr_number的顺序进行排列
    response_time = []
    for item in first_response_time_dict.keys():
        response_time.append(first_response_time_dict[item])
    close_time=[]
    for item in close_time_dict.keys():
        close_time.append(close_time_dict[item])
    return day_data, merge_result_dict,response_time, first_response_time_dict,close_time,close_time_dict, file_pr_dict


def prepare_temp_file(temp_data_path, origin_data_path, open_pr_index_list, day):
    file = open(temp_data_path, 'w+')
    for i in range(len(open_pr_index_list)):
        s = getline(origin_data_path, open_pr_index_list[i] + 1)
        file.write(s)
    file.close()
    print("【ranklib_baseline.py】保存第 " + str(day) + " 天的临时文件成功")


# 可显示使用循环, 注意enumerate从0开始计数，而line_number从1开始
def getline(the_file_path, line_number):
    if line_number < 1:
        return ''
    for cur_line_number, line in enumerate(open(the_file_path, 'rU')):
        if cur_line_number == line_number - 1:
            return line
    return ''


# 从模型计算出的排序文件获取模型的排序结果
def get_result_list(the_file_path):
    result = []
    for line in open(the_file_path):
        line_str = line.split(" ")
        result.append(int(line_str[2]))
    return result


# 根据已有数据得到排序结果
def model_forest(day_data, day, pr_number_index_dict, origin_data_path, temp_data_path, temp_sort_result_path,
                 model_path, jar_path):
    re_rank_str = "java -jar " + jar_path + " -load " + model_path + " -rank " + temp_data_path + " -indri " + temp_sort_result_path
    open_pr_list = []
    open_pr_index_list = []
    sort_result = []
    # 得到本日以及本日之前还处于开放状态的pr_number，并利用已训练好的模型，重新排序，并把排序的结果读取出来
    for key in day_data.keys():
        if key > day:
            continue
        else:
            # 获取当前天的所有openPR
            temp_pr_dict = day_data[key]
            for pr_key in temp_pr_dict:
                # 如果pr_number_index_dict中不含该pr_number或者该pr_number已经被关闭，则跳过
                if pr_number_index_dict.__contains__(pr_key) is False or temp_pr_dict[pr_key][
                    'closed_time'].date() < day:
                    continue
                else:
                    open_pr_list.append(pr_key)
                    # pr_number_index_dict.get(pr_key)用pr_number取出对应的index（pr在svm_rank_format_test_data.txt中的行数）
                    open_pr_index_list.append(pr_number_index_dict.get(pr_key))
    
    # 如果没有处于开放状态的PR，则直接返回
    if open_pr_list.__len__() == 0:
        return sort_result
    
    prepare_temp_file(temp_data_path, origin_data_path, open_pr_index_list, day)
    
    recv = os.popen(re_rank_str)
    print("【ranklib_baseline.py】模型计算中：")
    print("【ranklib_baseline.py】recv.read()=",recv.read())
    
    sort_result = get_result_list(temp_sort_result_path)
    return sort_result


# 对模型进行调用，同时将数据写入到文件中，方便后续统计
def alg_model_result(true_rate_label_dict, day_data, pr_number_index_dict, origin_data_path, temp_data_path,
                     temp_sort_result_path, model_path, jar_path,repo_name):
    ndcg_list = []
    day_list = []
    mrr_list = []
    kendall_list = []
    max_day = None
    min_day = None
    for day in day_data.keys():
        print("【ranklib_baseline.py】=================================日期:", day)
        # 获取每一天还处于open状态的pr列表顺序
        sort_result = model_forest(day_data, day, pr_number_index_dict, origin_data_path, temp_data_path,
                                   temp_sort_result_path, model_path, jar_path)
        if sort_result.__len__() == 0:
            print("【ranklib_baseline.py】在" + origin_data_path + "无相关pr")
            continue
        rank_sort = []
        true_sort = []
        # 获取从fifo中获取的每个列表的顺序
        for pr_number_result in sort_result:
            rank_sort.append(true_rate_label_dict[pr_number_result])
            true_sort.append(true_rate_label_dict[pr_number_result])
        true_sort.sort(reverse=True)
        ndcg_num = ndcg(true_sort, rank_sort, rank_sort.__len__(),form = "exp")
        mrr_num = mrr(true_sort, rank_sort)
        kendall_num = kendall_tau_distance(true_sort, rank_sort)
        print("【ranklib_baseline.py】pr_number排序:", sort_result)
        print("【ranklib_baseline.py】rank_sort:", rank_sort)
        print("【ranklib_baseline.py】true_sort:", true_sort)
        print("【ranklib_baseline.py】ndcg_num:", ndcg_num)
        print("【ranklib_baseline.py】mrr_num:", mrr_num)
        print("【ranklib_baseline.py】kendall_num:", kendall_num)
        if max_day is None or max_day < day:
            max_day = day
        if min_day is None or min_day > day:
            min_day = day
        day_list.append(day)
        ndcg_list.append(ndcg_num)
        mrr_list.append(mrr_num)
        kendall_list.append(kendall_num)

    headers = ['日期',
               'ndcg',
               'mrr',
               'kendall_tau_distance'
               ]
    row_data = []
    for i in range(len(day_list)):
        tmp = []
        tmp.append(day_list[i])
        tmp.append(ndcg_list[i])
        tmp.append(mrr_list[i])
        tmp.append(kendall_list[i])
        row_data.append(tmp)
    print("【ranklib_baseline.py】row_data=",row_data)
    # 保存数据到csv文件
    result_path="./result/ranklib/"+repo_name+"/"
    path_exists_or_create(result_path)
    with open(result_path+ repo_name + "_" + alg_name + "_result.csv",
            'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(headers)
        for item in row_data:
            writer.writerow(item)


# 训练模型
def train_model(alg_name, alg_index, train_data_path, test_data_path, model_path):
    rank_model_str = "java -jar " + jar_path + " -train " + train_data_path + " -test " + test_data_path + " -ranker " + str(
        alg_index) + " -metric2t NDCG@10 -metric2T NDCG@10 -lr 0.01 -save " + model_path
    recv = os.popen(rank_model_str)
    print("【ranklib_baseline.py】===============训练模型+" + alg_name + "======================")
    print("【ranklib_baseline.py】训练的命令是：" + rank_model_str)
    print("【ranklib_baseline.py】recv.read()=",recv.read()) # 打印命令行在控制台输出的结果


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    repo_name =get_repo_name()#"scikit-learn"#"moby"#"cocos2d-x"#"netbeans"#"yii2"##"dubbo"#"react"#"tensorflow"#"opencv"#"phoenix"#"helix"#"terraform"#"Ipython"#"kuma"#"incubator-heron"#"Katello"#"zipkin"#"incubator-heron"# "Katello"#"zipkin"#"yii2"#"dubbo"#"react"#"tensorflow"# "opencv"#"phoenix"#"guacamole-client"# "helix"#"terraform"#"Ipython"#"kuma"#"incubator-heron"#"Katello" #"salt"  # "zipkin"#"angular.js"  # "symfony"# #"tensorflow"#"spring-boot"#"spring-framework"#"rails"
    # ranklib所能调的库
    alg_dict = {
        # 0: "MART",
        # 1: "RankNet",
        # 2: "RankBoost",
        # 3: "AdaRank",
        # 4: "Coordinate_Ascent",
        # 6: "LambdaMART",
        # 7: "ListNet",
        # 8: "Random_Forests"
        0:"Random_Forests"
    }
    for alg_index in alg_dict.keys():
        alg_name = alg_dict.get(alg_index)
        # 测试模型性能的文件路径
        jar_path = "./baselines/RankLib-2.16.jar"
        file_path = "./data/rank_data/" + repo_name + "/"
        path_exists_or_create(file_path)
        origin_data_path = file_path + repo_name + "_svm_rank_format_test_data.txt"
        temp_data_path = file_path + repo_name + "_temp_svm_rank_format_data.txt"
        temp_sort_result_path = file_path + repo_name + "_myScoreFile.txt"

        model_path = "./model/rank_model/" + repo_name + "/"
        path_exists_or_create(model_path)
        model_path = model_path + repo_name + "_" + alg_name + "_model.txt"
        # 训练模型的文件路径
        train_data_path =file_path + repo_name + "_svm_rank_format_train_data.txt"
        test_data_path = file_path + repo_name + "_svm_rank_format_test_data.txt"
        # 首先运行算法训练模型并保存模型
        train_model(alg_name, alg_index, train_data_path, test_data_path, model_path)
        print("【ranklib_baseline.py】alg_name=",alg_name + "模型训练完成==========")
        day_data, merge_dict,response_time, first_response_time_dict,close_time,close_time_dict, pr_number_index_dict = \
        get_data_by_repo_name_and_origin_data_path(origin_data_path, repo_name)
        true_response_rate_label_dict = get_true_order_dict(response_time, first_response_time_dict)
        true_close_rate_label_dict = get_true_order_dict(close_time, close_time_dict)
        true_rate_label_dict = {}
        for key in merge_dict.keys():
            true_rate_label_dict[key] = (merge_dict[key]+true_response_rate_label_dict[key]+true_close_rate_label_dict[key])/3.0

        alg_model_result(true_rate_label_dict, day_data, pr_number_index_dict, origin_data_path, temp_data_path,
                         temp_sort_result_path, model_path, jar_path,repo_name)
