import xlsxwriter
import os

# https://xlsxwriter.readthedocs.io/
baseDir = "C:\\Users\\Administrator\\Desktop\\excel"
excelName = 'hello2.xlsx'
if not os.path.exists(baseDir):
    os.makedirs(baseDir)
workbook = xlsxwriter.Workbook(os.path.join(baseDir,excelName))  # 创建一个Excel文件
worksheet = workbook.add_worksheet()  # 创建一个sheet
header_format = workbook.add_format({
    'bold': True, 'font_size': 15,'font_name': '宋体'
})
header_format.set_align('center')  # 水平对齐
header_format.set_align('vcenter')  # 垂直对齐
header_format.set_text_wrap()  # 内容换行

body_format = workbook.add_format({
    'bold': False, 'font_size': 12,'font_name': '宋体'
})
body_format.set_align('left')  # 水平对齐
body_format.set_align('vcenter')  # 垂直对齐
body_format.set_text_wrap()  # 内容换行
# 列宽
worksheet.set_column('A:J', 20)

json = [{"bookName": "断舍离", "price": "20.6"}, {
    "bookName": "算法之美"}, {"bookName": "算法之美", "price": "21.5"}, {"price": "22.5"}]
# 自动过滤
worksheet.autofilter('A1:B'+str(len(json)+1))

# https://www.jianshu.com/p/c13b24d04730
# 向 excel 中写入数据
data1 = ['书名', '价格']
worksheet.write_row('A1', data1, header_format)
for index, item in enumerate(json):
    data = []
    data.append(item.get("bookName", ''))
    data.append(item.get("price", ''))
    worksheet.write_row('A'+str(2+index), data,body_format)
workbook.close()
