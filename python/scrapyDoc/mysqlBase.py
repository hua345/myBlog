import mysql.connector
# import pymysql.cursors

config = {
    'user': 'root',
    'password': 'xxx',
    'host': '192.168.137.128',
    'port': 3306,
    'database': 'fang'
}
# 创建一个连接
mysqlConn = mysql.connector.connect(**config)
mysqlCur = mysqlConn.cursor(buffered=True)
# mysqlConn = pymysql.connect(**config)
# mysqlCur = mysqlConn.cursor()
# 执行查询语句
mysqlCur.execute("SELECT CURDATE()")
# 获取结果
row = mysqlCur.fetchone()
print("Current date is: {0}".format(row[0]))
mysqlCur.execute("SELECT CURDATE()")
# 插入数据
val = ("断舍离", "20",)
sql = " insert into book (book_name,price) VALUES (%s,%s) "
print(sql % val)
mysqlCur.execute(sql, val)
print(mysqlCur.rowcount)
# 查询结果
mysqlCur.execute('select * from book where book_name = %s', ('断舍离',))
print(mysqlCur.fetchall())
# 提交事务:
mysqlConn.commit()
# 关闭连接
mysqlConn.close()
