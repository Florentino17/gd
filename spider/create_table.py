import pymysql
from  GetDbName import getDataBaseName
import pandas as pd
import datetime
dbName=getDataBaseName()

def connect_to_database():
    db=pymysql.connect(host='localhost',user='root',password='123456',charset='utf8',db=dbName)
    cursor=db.cursor()
    return db,cursor


def create_table_pr_repo():

    #连接数据库，并打开wzg数据库（数据库已创建）
    db,cursor=connect_to_database()

    try:
        #创建student表，并执行
        sql='''create table pr_repo(
            repo_id varchar(255)  NOT NULL,
            full_name mediumtext,
            repo_name mediumtext,
            owner_name mediumtext,
            owner_type mediumtext,
            team_size int,
            project_created_at datetime ,
            project_updated_at datetime ,
            project_pushed_at datetime ,
            watchers int,
            stars int,
            use_language mediumtext,
            languages mediumtext,
            project_domain mediumtext,
            contributor_num int,
            forks_count int,
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
        self_id int NOT NULL auto_increment,
        pr_number int ,
        pr_url mediumtext,
        repo_name mediumtext,
        pr_user_id mediumtext,
        pr_user_name mediumtext,
        pr_author_association mediumtext,
        title mediumtext,
        body mediumtext,
        labels mediumtext,
        state mediumtext,

        created_at datetime ,
        updated_at datetime ,
        closed_at datetime ,
        merged_at datetime ,
        merged int,
        mergeable int,
        mergeable_state mediumtext,
        merge_commit_sha mediumtext,
        assignees_content mediumtext,
        requested_reviewers_content mediumtext,

        comments_number int,
        comments_content mediumtext,
        review_comments_number int,
        review_comments_content mediumtext,
        commit_number int,
        commit_content mediumtext,
        changed_file_num int,
        total_add_line int,
        total_delete_line int,

        primary key(self_id)
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
        file_id int NOT NULL auto_increment,
        pr_number int, 
        repo_name mediumtext, 
        changed_file_name mediumtext,
        sha mediumtext, 
        changed_file_status mediumtext, 
        lines_added_num int, 
        lines_deleted_num int, 
        lines_changed_num int,
        contain_patch int, 
        patch_content mediumtext,

        primary key(file_id)
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
        user_name mediumtext, 
        followers_num int,
        followers mediumtext, 
        following_num int,
        following mediumtext, 
        public_repos_num int, 
        author_association_with_repo mediumtext,

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

def create_table_pr_all():
    #连接数据库，并打开wzg数据库（数据库已创建）
    db,cursor=connect_to_database()

    try:
        #创建student表，并执行
        sql='''create table pr_all(
        pid int NOT NULL, 
        
        project mediumtext, 
        change_id int,
        created datetime, 
        subject mediumtext,
        author_experience double, 

        author_merge_ratio double, 
        author_changes_per_week double,
        author_merge_ratio_in_project double,
        total_change_num int,
        author_review_num int,

        is_reviewer int,
        author_subsystem_change_num int,
        author_subsystem_change_merge_ratio double,
        author_avg_rounds double,
        author_contribution_rate double,

        author_merged_change_num int,
        author_abandoned_changes_num int,
        author_avg_duration double,
        description_length int,
        is_documentation int,

        is_bug_fixing int,
        is_feature int,
        is_improve int,
        is_refactor int,
        commit_num int,

        comment_num int,
        comment_word_num int,
        last_comment_mention int,
        has_test_file int,
        description_readability double,

        is_responded int,
        first_response_duration double,
        project_changes_per_week double,
        project_merge_ratio double,
        changes_per_author int,

        project_author_num int,
        project_duration_per_merged_change int,
        project_commits_per_merged_change int,
        project_comments_per_merged_change int,
        project_file_num_per_merged_change int,

        project_churn_per_merged_change int,
        project_duration_per_abandoned_change int,
        project_commits_per_abandoned_change int,
        project_comments_per_abandoned_change int,
        project_file_num_per_abandoned_change int,

        project_churn_per_abandoned_change int,
        project_additions_per_week double,
        project_deletions_per_week double,
        workload int,
        num_of_reviewers int,

        num_of_bot_reviewers int,
        avg_reviewer_experience double,
        avg_reviewer_review_count double,
        review_avg_rounds double,
        review_avg_duration double,

        lines_added int,
        lines_updated int,
        lines_deleted int,
        files_added double,
        files_deleted int,

        files_modified int,
        num_of_directory int,
        modify_entropy int,
        subsystem_num int,
        language_num int,

        file_type_num int,
        segs_added int,
        segs_deleted int,
        segs_updated int,
        modified_code_ratio double,

        test_churn int,
        src_churn int,
        degree_centrality double,
        closeness_centrality double,
        betweenness_centrality double,

        eigenvector_centrality double,
        clustering_coefficient double,
        k_coreness int,
        avg_score int,
        closed datetime,
        
        user_id int,
        status int,
        time double,
        rounds int,

        primary key(pid)
        )default charset=utf8;'''
        cursor.execute(sql)

    #发生错误时，打印报错原因
    except Exception as e:
        print(e)

    #无论是否报错都执行
    finally:
        cursor.close()
        db.close()
def create_table_pr_all_file():
    #连接数据库，并打开wzg数据库（数据库已创建）
    db,cursor=connect_to_database()

    try:
        #创建student表，并执行
        sql='''create table pr_all_file(
        file_num_id int NOT NULL, 
        
        id_in_all int, 
        file_name mediumtext,
        primary key(file_num_id)
        )default charset=utf8;'''
        cursor.execute(sql)

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

def insert_pr_all_test():
    
    data = pd.read_csv("E://Desktop//data//Eclipse.csv")



    def shijian(dd):
        dd = datetime.datetime.strptime(dd, "%Y-%m-%d %H:%M:%S")
        return dd



    row_num=data.shape[0]
    line_num=data.shape[1]
    print(row_num,line_num)

# for i in range(0,row_num):
#     for j in range(0,line_num):

    for i in range(0,3):
        
        data.iloc[i,2]=shijian(data.iloc[i,2].split('.')[0])
        print(type(data.iloc[i,2]))
    db,cursor=connect_to_database()
    try:
    #1
        insert_sql='''
        insert into pr_all (pid,created) values(%s,%s)
        '''
        # cursor.execute(insert_sql)
        values=(1,data.iloc[1,2])
        print(type(values))
        cursor.execute(insert_sql, values)
        #将数据提交给数据库（加入数据，修改数据要先提交）
        db.commit()
    except Exception as e:
        print(e)

    #无论是否报错都执行
    finally:
        cursor.close()
        db.close() 

if __name__ == '__main__':
    
    # create_table_pr_repo()
    # print("创建表pr_repo")

    # create_table_pr_self()
    # print("创建表pr_self")

    # create_table_pr_file()
    # print("创建表pr_file")

    # create_table_pr_user()
    # print("创建表pr_user")

    # create_table_pr_all()
    # print("创建表pr_all")

    # delete_all_records()
    # print("删除全部数据")

    # insert_into_table()
    # print("插入数据")
    # create_table_pr_all()
    create_table_pr_all_file()
    # insert_pr_all_test()
    print()


