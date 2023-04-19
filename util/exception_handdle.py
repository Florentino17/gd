# 处理无法获得的PR，然后记录到文件中，记录格式如下，时间|PRNumber，时间|PR编号
import os
import time


# 将异常写到文件中
def write_file(pr_number, project_name, exception, filename):
    current_path = os.getcwd() + '\\exception_data\\'  # 获取当前路径
    isExists=os.path.exists(current_path)
    # 判断文件夹是否存在，不存在则创建
    if(isExists):
        print("【util/str_utils/exception_handdle.py】",current_path+"文件夹已经存在")
    else:
        os.makedirs(current_path)
        print("【util/str_utils/exception_handdle.py】",current_path+"文件夹创建成功")
    
    path = current_path + filename  # 在当前路径创建名为test的文本文件
    now_time = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))  # 获取当前时间
    context = project_name + ", " + pr_number.__str__() + ', ' + now_time + ', ' + exception + "\n"
    if os.path.exists(path):
        print("【util/str_utils/exception_handdle.py】",path + ' is already exist')
        print('【util/str_utils/exception_handdle.py】context is :' + context)
        file = open(path, 'a+')
        file.write(context)
    else:
        print("【util/str_utils/exception_handdle.py】创建文件：" + path)
        file = open(path, 'a+')
        file.write(context)
    file.close()

# 写入数据库时，去操作一下
# write_file(100, 'jsonjson', "404", 'repo_exception.csv')
#
# print("当前时间： ", time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time())))
