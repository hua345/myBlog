import xlsxwriter
workbook = xlsxwriter.Workbook('hello2.xlsx')  #创建一个Excel文件
worksheet = workbook.add_worksheet()               #创建一个sheet

# https://www.jianshu.com/p/c13b24d04730
#向 excel 中写入数据
data1 = ['年份','数量','剩余数量']
data2 = ['2013','100','50']
worksheet.write_row('A1',data1)
worksheet.write_row('A2',data2)
workbook.close()