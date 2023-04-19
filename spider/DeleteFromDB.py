from  GetDbName import getDataBaseName
dbName=getDataBaseName()
import pymysql as db
#删除


# 打开数据库连接
# conn = pymysql.connect(host,port,user,passwd,db,charset)
try:
    # 使用 cursor() 方法创建一个游标对象 cursor
    database = db.connect(host='localhost', 
                            port=3306, 
                            user='root', 
                            password='123456', 
                            db=dbName, 
                            charset='utf8')
    sql =('delete from pr_file where  pr_number=3450')
        # 创建游标对象
    cursor = database.cursor()
        # 利用游标对象进行操作
    cursor.execute(sql)

    cursor = database.cursor()
    # id = 16066
    # SQL 删除语句
    
    # 执行SQL语句
    cursor.execute(sql)
    # 确认修改
    database.commit()
    # 关闭游标
    cursor.close()
    # 关闭链接
    database.close()
    print("删除成功")
except:
    print("删除失败")



