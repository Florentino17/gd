import pymysql as db
import requests
import os
import sys
import time
import json

# 将上一级目录添加到系统环境变量中，这样可以调用util内的工具包
sys.path.append(os.getcwd())   #i 方便调用util内的工具包

from util.access_token import get_token
from util.time_utils import time_reverse    #i   时间转换 # 2021-10-08T01:11:34Z时间转换2021-10-08 01:11:34
from util.exception_handdle import write_file   #i 异常处理将异常写到文件中
from  GetDbName import getDataBaseName
dbName=getDataBaseName()


# 统计url中含有的元素数量
def findUrlJsonCount(url_str,headers):   #i 统计url中含有的元素数量
    url_str = url_str + "?per_page=100&anon=true&page=" #每页最多100个元素   #i 每页最多100个元素
    print("【repo】 repo: findUrlJsonCount  url_str  ",url_str)
    page = 1
    count = 0
    while 1:
        temp_url_str = url_str + page.__str__()
        print("【repo】 repo: temp_url_str=",temp_url_str)
        url_r = requests.get(temp_url_str, headers=headers)
        url_json = url_r.json() #转为json格式
        if len(url_json) < 100:
            count = count + len(url_json)
            return count
        else:
            count = count + 100
            page = page + 1
    return count


# 封装成一个方法，方便外部调用
def get_repo_info(index, owner_name, repo_name,headers):
    # repo url拼接
    repo_url = "https://api.github.com/repos/" + owner_name + "/" + repo_name
    # 组织url 拼接，主要是为了找多少人 page后面的用拼接来确定到底有多少人，省的去页面爬了，太麻烦。
    org_url = "https://api.github.com/orgs/" + owner_name + "/members"
    print("【repo】 repo_url=",repo_url)
    print("【repo】 org_url=",org_url)
    # 数据操作部分
    # SQL语句书写
    sql = """insert into pr_repo(
        repo_id,
        full_name,
        repo_name,
        owner_name,
        owner_type,
        team_size,
        project_created_at,
        project_updated_at,
        project_pushed_at,
        watchers,
        stars,
        use_language,
        languages,
        project_domain,
        contributor_num,
        forks_count)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """

    # 连接到数据库
    # database = db.connect(host='172.19.241.129', port=3306, user='root', password='root', db='pr_second',charset='utf8')
    database = db.connect(host='localhost', 
                          port=3306, 
                          user='root', 
                          password='123456', 
                          db=dbName, 
                          charset='utf8')
    # 创建游标对象
    cursor = database.cursor()
    # 利用游标对象进行操作
    cursor.execute('select version()') #查看数据库版本
    data = cursor.fetchone()

    print('【repo】 Database version:%s' % data)


    while index < 1:#同一个仓库信息只能插入一次
        try:
            repo_r = requests.get(repo_url, headers=headers)
            print("【repo】 repo_url: " + repo_url + "  Status Code:", repo_r.status_code)#打印状态码
        except Exception as e:
            # 如果发生错误则回滚
            print("【repo】 网络连接失败: repo_url: ", repo_url, "org_url: ", org_url)
            filename = 'repo_exception.csv'
            write_file(index, repo_name + "-" + owner_name,
                       str(e) + ("网络连接失败: user_name: " + repo_name + "owner_name: " + owner_name),
                       filename)
            print("【repo】 打印报错信息",e) #打印报错信息

            access_token = get_token()
            headers = {
                'Authorization': 'token ' + access_token
            }
            time.sleep(10)  #暂停10秒
            continue
        
        
            # 如果返回的状态码以2开头，则说明正常此时去写入到数据库中即可
        if repo_r.status_code >= 200 and repo_r.status_code < 300:
            repo_json_str = repo_r.json()
            length_repo_json = len(repo_json_str)
            print("【repo】 repo_json_str:", length_repo_json)
            # 基础数据
            repo_id = repo_json_str["id"]
            full_name = repo_json_str["full_name"]
            owner_type = repo_json_str["owner"]["type"]
            created_at = repo_json_str["created_at"]
            updated_at = repo_json_str["updated_at"]
            pushed_at = repo_json_str["pushed_at"]
            watchers = repo_json_str["subscribers_count"]
            stars = repo_json_str["stargazers_count"]
            # 获取主要language
            use_language = repo_json_str["language"]
            forks_count = repo_json_str["forks"]
            # 获取所有languages所对应的json
            languages_r = requests.get(repo_json_str["languages_url"], headers=headers)
            languages_json = json.dumps(languages_r.json())  #将字典转化为json格式字符串
            # 获取project_domain并转换为json格式
            topics = {}
            for i in range(0, repo_json_str["topics"].__len__()):
                topics[i] = repo_json_str["topics"][i]

            project_domain = json.dumps(topics)   #将字典转化为json格式字符串
            # 获取contributor的数量
            contributor_num = findUrlJsonCount(repo_json_str["contributors_url"],headers)
            team_size = None
            # team_size的数量统计
            if repo_json_str["owner"]["type"].__eq__("Organization"):
                team_size = findUrlJsonCount(org_url,headers)

        else: #返回的状态码不以2开头
            filename = 'repo_exception.csv'
            write_file(index, "user",
                       ("第" + str(index) + "行连接有问题: " + "repo_name:" + repo_name),
                       filename)
            continue

        index = index + 1 #循环一次后必跳出循环
        try:
            sqlData = (
                repo_id,
                full_name,
                repo_name,
                owner_name,
                owner_type,
                team_size,
                time_reverse(created_at),
                time_reverse(updated_at),
                time_reverse(pushed_at),
                watchers,
                stars,
                use_language,
                languages_json,
                project_domain,
                contributor_num,
                forks_count)
            print("【repo】 ",
                " repo_id full_name,repo_name,owner_name,owner_type,team_size,time_reverse(created_at),time_reverse(updated_at),time_reverse(pushed_at), watchers,stars,use_language,languages_json, project_domain,contributor_num,forks_count",
                sqlData)
            # 执行sql语句
            cursor.execute(sql, sqlData)
            # 提交到数据库执行
            database.commit()
            print("【repo】 第", index, "行数据插入数据库成功: ", repo_name)
        except Exception as e:
            # 如果发生错误则回滚
            print("【repo】 第", index, "行数据插入数据库失败: ", "repo_name:", repo_name)
            filename = 'repo_exception.csv'
            write_file(index, "user",
                       ("第" + str(index) + "行数据插入数据库失败: " + "repo_name:" + repo_name + str(e)),
                       filename)
            print("【repo】 报错信息",e)
            database.rollback()
            continue
        # 关闭数据库连接
        database.close()


# get_repo_info(index=0, owner_name="activemerchant", repo_name="active_merchant",headers={'Authorization': 'token ' + get_token()})
# get_repo_info(index=0, num=10, owner_name="wozhendeshuai", repo_name="nju_pr_project",headers={'Authorization': 'token ' + get_token()})