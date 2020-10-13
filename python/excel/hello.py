import xlwt

# 1. 创建workbook对象
workbook = xlwt.Workbook(encoding="utf-8")
# 2. 创建工作表
worksheet = workbook.add_sheet("sheet1")
# 3. 写入数据，第一行参数”行“，第二个参数”列“，第三个参数内容
worksheet.write(0, 0, "hello")  # 
# 4. 保存数据表
workbook.save("hello.xls")