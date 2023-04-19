##从sql获取数据
import pymysql

def getDataFromSql(sqlOrder):

    ##连接数据库
    conn=pymysql.connect(
        # host="172.19.241.129",
        # port=3306,#端口号
        # user="root",#数据库用户
        # password="root",#数据库密码
        # database="pr_second"#要连接的数据库名称
        # host="127.0.0.1",
        host="localhost",
        port=3306,#端口号
        user="root",#数据库用户
        password="123456",#数据库密码
        database="gd_eclipse"#要连接的数据库名称
    )

#prp_test
#gd_zendframework
#gd_ipython
#gd_tensorflow
#gd_katello
#gd_terraform
#gd_opencv
#gd_cocos2d-x

    cursor=conn.cursor()#游标


    ###从username数据库获取所有的name
    sql=sqlOrder
    cursor.execute(sql)
    data=cursor.fetchall()
    return data