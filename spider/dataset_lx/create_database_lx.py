#引入decimal模块
import pymysql

#连接数据库
db=pymysql.connect(host='localhost',user='root',password='123456',charset='utf8')

#创建一个游标对象（相当于指针）
cursor=db.cursor()

#执行创建数据库语句
cursor.execute('create schema wfh default charset=utf8;')
cursor.execute('show databases;')

#fetchone获取一条数据（元组类型）
print(cursor.fetchone())
#现在指针到了[1]的位置

#fetchall获取全部数据（字符串类型）
all=cursor.fetchall()
for i in all:
    print(i[0])

#关闭游标和数据库连接
cursor.close()
db.close()



'''
一、简介

MySQL在5.5.3之后增加了这个utf8mb4的编码，mb4就是most bytes 4的意思，专门用来兼容四字节的unicode。utf8mb4是utf8的超集，
除了将编码改为utf8mb4外不需要做其他转换。当然，为了节省空间，一般情况下使用utf8也就够了。

'''