import pymysql

#连接数据库，并打开wzg数据库（数据库已创建）
db=pymysql.connect(host='localhost',user='root',password='123456',charset='utf8',db='wfh')

#创建游标对象
cursor=db.cursor()

try:
    #创建student表，并执行
    sql='''create table student(
       SNO char(10),
       SNAME varchar(20) NOT NULL,
       SSEX varchar(1),
       primary key(SNO)
       )default charset=utf8;'''
    cursor.execute(sql)
	
    #插入一条数据，并执行
    insert_sql='''
    insert into student values('200303016','王智刚','男'),('20030001','小明','男')
    '''
    cursor.execute(insert_sql)
	
    #将数据提交给数据库（加入数据，修改数据要先提交）
    db.commit()
	
    #执行查询语句
    cursor.execute('select * from student')
	
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