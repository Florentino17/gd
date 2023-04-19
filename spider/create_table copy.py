import pymysql
def connect_to_database():
    db=pymysql.connect(host='localhost',user='root',password='123456',charset='utf8',db='prp_test')
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




def create_table_pr_self():

    #连接数据库，并打开wzg数据库（数据库已创建）
    db,cursor=connect_to_database()

    try:
        #创建student表，并执行
        sql='''create table pr_self(
        pr_number varchar(255) NOT NULL,
        pr_url varchar(255),
        repo_name varchar(255),
        pr_user_id varchar(255),
        pr_user_name varchar(255),
        pr_author_association varchar(255),
        title varchar(255),
        body varchar(255),
        labels varchar(255),
        state varchar(255),

        created_at varchar(255),
        updated_at varchar(255),
        closed_at varchar(255),
        merged_at varchar(255),
        merged varchar(255),
        mergeable varchar(255),
        mergeable_state varchar(255),
        merge_commit_sha varchar(255),
        assignees_content varchar(255),
        requested_reviewers_content varchar(255),

        comments_number int,
        comments_content TEXT(60000),
        review_comments_number int,
        review_comments_content varchar(255),
        commit_number int,
        commit_content TEXT(60000),
        changed_file_num int,
        total_add_line varchar(255),
        total_delete_line varchar(255),

        primary key(pr_number)
        )default charset=utf8;'''
        cursor.execute(sql)
        
    #发生错误时，打印报错原因
    except Exception as e:
        print(e)

    #无论是否报错都执行
    finally:
        cursor.close()
        db.close()

def create_table_pr_file():

    #连接数据库，并打开wzg数据库（数据库已创建）
    db,cursor=connect_to_database()

    try:
        #创建student表，并执行
        sql='''create table pr_file(
        pr_number int NOT NULL, 
        repo_name varchar(255), 
        changed_file_name varchar(255),
        sha varchar(255), 
        changed_file_status varchar(255), 
        lines_added_num int, 
        lines_deleted_num int, 
        lines_changed_num int,
        contain_patch varchar(255), 
        patch_content text(60000),

        primary key(pr_number)
        )default charset=utf8;'''
        cursor.execute(sql)
        
        

    #发生错误时，打印报错原因
    except Exception as e:
        print(e)

    #无论是否报错都执行
    finally:
        cursor.close()
        db.close()


def create_table_pr_user():

    #连接数据库，并打开wzg数据库（数据库已创建）
    db,cursor=connect_to_database()

    try:
        #创建student表，并执行
        sql='''create table pr_user(
        user_id varchar(255) NOT NULL, 
        user_name varchar(255), 
        followers_num int,
        followers TEXT(60000), 
        following_num int,
        following TEXT(60000), 
        public_repos_num int, 
        author_association_with_repo varchar(255),

        primary key(user_id)
        )default charset=utf8;'''
        cursor.execute(sql)

    #发生错误时，打印报错原因
    except Exception as e:
        print(e)

    #无论是否报错都执行
    finally:
        cursor.close()
        db.close()
def insert_into_table():
    db,cursor=connect_to_database()
    try:
    #1
        insert_sql='''
        insert into pr_repo values('1','2','3','3','3','3','3','1','6','6','6','6','8','8','8','8'),
        ('56','22','33','3','3','3','3','1','6','6','6','6','8','8','8','8')
        '''
        cursor.execute(insert_sql)
        
        #将数据提交给数据库（加入数据，修改数据要先提交）
        db.commit()
        
        #执行查询语句
        cursor.execute('select * from pr_repo')
        
        #打印全部数据
        all=cursor.fetchall()
        for i in all:
            print(i)
    #2
        insert_sql='''
        insert into pr_self values('1','2','3','3','3','3','3','1','6','6','6','6','8','8','8','8','8','8','8','8','8','8','8','8','8','8','8','8','8'),
        ('56','22','33','3','3','3','3','1','6','6','6','6','8','8','8','8','33','33','33','33','33','33','33','33','33','33','33','33','33')
        '''
        cursor.execute(insert_sql)
        
        #将数据提交给数据库（加入数据，修改数据要先提交）
        db.commit()
        
        #执行查询语句
        cursor.execute('select * from pr_self')
        
        #打印全部数据
        all=cursor.fetchall()
        for i in all:
            print(i)
    #3
        insert_sql='''
        insert into pr_file values('1','2','3','3','3','3','3','1','6','8'),
        ('56','22','33','3','3','3','3','1','6','6')
        '''
        cursor.execute(insert_sql)
        
        #将数据提交给数据库（加入数据，修改数据要先提交）
        db.commit()
        
        #执行查询语句
        cursor.execute('select * from pr_file')
        
        #打印全部数据
        all=cursor.fetchall()
        for i in all:
            print(i)
    #4
        insert_sql='''
        insert into pr_user values('1','2','3','3','3','3','3','1'),
        ('56','22','33','3','3','3','3','1')
        '''
        cursor.execute(insert_sql)
        db.commit()
        #执行查询语句
        cursor.execute('select * from pr_user')
        #打印全部数据
        all=cursor.fetchall()
        for i in all:
            print(i)

    #发生错误时，打印报错原因
    except Exception as e:
        print(e)

    #无论是否报错都执行
    finally:
        cursor.close()
        db.close()
def delete_all_records():
    db,cursor=connect_to_database()
    try:
        cursor.execute('delete from pr_repo')
        cursor.execute('delete from pr_self')
        cursor.execute('delete from pr_file')
        cursor.execute('delete from pr_user')
        db.commit() 
    #发生错误时，打印报错原因
    except Exception as e:
        print(e)

    #无论是否报错都执行
    finally:
        cursor.close()
        db.close()
        
if __name__ == '__main__':
    
    print("it is copy")
    print("it is copy")
    print("it is copy")
    create_table_pr_repo()
    print("创建表pr_repo")

    create_table_pr_self()
    print("创建表pr_self")

    create_table_pr_file()
    print("创建表pr_file")

    create_table_pr_user()
    print("创建表pr_user")

    # insert_into_table()
    # print("插入数据")

    # delete_all_records()
    # print("删除全部数据")
    print()