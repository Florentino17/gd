# file_num='1'


# file_num=(int)(file_num)
# print(file_num+32)

# print(300//54)



# import datetime

# starttime = datetime.datetime.now()
# sum=0
# for i in range(0,100000000):
#     sum=1
# endtime = datetime.datetime.now()
# print("时长：",end="")
# print (endtime - starttime)  







import pymysql
def connect_to_database():
    db=pymysql.connect(host='server.natappfree.cc',user='root',port=39859,password='123456',charset='utf8',db='remote_test')
    cursor=db.cursor()
    return db,cursor


def create_table_pr_repo():

    #连接数据库，并打开wzg数据库（数据库已创建）
    db,cursor=connect_to_database()

    try:
        #创建student表，并执行
        sql='''create table pr_repo(
            repo_id varchar(255) NOT NULL,
            full_name varchar(255),
            repo_name varchar(255),
            owner_name varchar(255),
            owner_type varchar(255),
            team_size varchar(255),
            project_created_at varchar(255),
            project_updated_at varchar(255),
            project_pushed_at varchar(255),
            watchers varchar(255),
            stars varchar(255),
            use_language varchar(255),
            languages varchar(255),
            project_domain varchar(255),
            contributor_num varchar(255),
            forks_count varchar(255),
            primary key(repo_id)
        )default charset=utf8;'''
        cursor.execute(sql)
        
    #发生错误时，打印报错原因
    except Exception as e:
        print(e)

    #无论是否报错都执行
    finally:
        cursor.close()
        db.close()





        
if __name__ == '__main__':
    

    create_table_pr_repo()
    print("[remote]创建表pr_repo")


    print()