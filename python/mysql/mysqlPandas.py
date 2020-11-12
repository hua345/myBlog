import numpy as np
import pandas as pd
from sqlalchemy import create_engine
# pip3 install pandas
# pip3 install sqlalchemy
# pip3 install pymysql
# 按实际情况依次填写MySQL的用户名、密码、IP地址、端口、数据库名
engine = create_engine('mysql+pymysql://root:FangFang520%@192.168.137.129:3306/db_example')

# MySQL导入DataFrame
# 填写自己所需的SQL语句，可以是复杂的查询语句
sql_query = 'select * from company;'
# 使用pandas的read_sql_query函数执行SQL语句，并存入DataFrame
print(pd)
df_read = pd.read_sql_query(sql_query, engine)
print(df_read)


