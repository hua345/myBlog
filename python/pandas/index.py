import numpy as np
import pandas as pd
from pandas import Series,DataFrame
# Series带标签的一维同构数组
# Series的index是可变的，而dict字典的key值是不可变的。
# DataFrame带标签的，大小可变的，二维异构表格
arr1 = np.arange(1,10)
print(Series(np.arange(1,10)))
data = Series([1,2,3,4],index = ['a','b','c','d'])
print(data)

data = {'book':['哈佛幸福公开课','断舍离','刻意练习'],'price':['21','22','23']}
df = DataFrame(data, columns=['book','price'])
print(df)
print(df.describe())

#获取数据
# 选择单列，产生 Series
print(df['book'])
# 用 [ ] 切片行：
print(df[0:1])

# 用标签提取一行数据
print(df.loc[0])
# 用标签选择列数据

df.to_excel('book.xlsx',index=False, sheet_name='Sheet1')
pd.read_excel('book.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
