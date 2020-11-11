import mysql.connector
import json
# pip3 install mysql-connector-python
# 连接数据库
config = {
    'user': 'root',
    'password': 'xxx',
    'host': '192.168.137.129',
    'port': '3306',
    'database': 'db_example'
}

json_data = {}
with open('./data.json', 'r', encoding='utf8')as fp:
    json_data = json.load(fp)[0]
    print(json_data)
    fp.close()


con = mysql.connector.connect(**config)
mycursor = con.cursor(buffered=True)
# 查询这里面所有的人：
val = (json_data["businessRegistration"]["socialCreditCode"],)
sql = "SELECT * FROM company where social_credit_code = %s "
print(sql % val)
mycursor.execute(sql, val)
data = mycursor.fetchone()  # fetchone() 获取一条记录
if data:
    print(data)
    updateVal = (json_data["companyName"], json_data["companyPhone"],
                 json_data["companyEmail"], json_data["officialWebsite"], json_data["companyAddress"], json_data["companyProfile"], data[0])
    updateSql = "UPDATE company SET company_name = %s, company_phone = %s, company_email = %s, official_website = %s, company_address = %s, company_profile = %s,update_at = now() WHERE id = %s ;"
    print(updateSql % updateVal)
    mycursor.execute(updateSql, updateVal)
    companyRegistration = json_data["businessRegistration"]
    registeredCapital = companyRegistration["registeredCapital"].replace(
        "万(元)", "").replace(",", "")
    paidInCapital = companyRegistration["paidInCapital"]
    if '-' == paidInCapital:
        paidInCapital = None
    operatingPeriod = companyRegistration["operatingPeriod"]
    operatingPeriodList = operatingPeriod.split("至")
    operatingPeriodBegin = operatingPeriodList[0].strip()
    operatingPeriodEnd = operatingPeriodList[1].strip()
    updateDetailVal = (companyRegistration["legalRepresentative"], companyRegistration["operatingStatus"], registeredCapital,
                       paidInCapital, companyRegistration["industry"], companyRegistration[
                           "socialCreditCode"], companyRegistration["taxpayerIdentificationNumber"],
                       companyRegistration["businessRegistrationNumber"], companyRegistration[
                           "organizationCode"], companyRegistration["registrationAuthority"],
                       companyRegistration["establishmentDate"], companyRegistration[
                           "enterpriseType"], operatingPeriodBegin, operatingPeriodEnd,
                       companyRegistration["administrativeDivisions"], companyRegistration[
                           "annualInspectionDate"], companyRegistration["registeredAddress"],
                       companyRegistration["businessScope"], data[0])
    updateDetailSql = "UPDATE db_example.company_registration SET legal_representative = %s, operating_status = %s, registered_capital = %s, paidIn_capital = %s, industry = %s, social_credit_code = %s, taxpayer_identification_number = %s, company_registration_number = %s, organization_code = %s, registration_authority = %s, establishment_date = %s, enterprise_type = %s, operating_period_begin = %s, operating_period_end = %s, administrative_divisions = %s, annualInspection_date = %s, registered_address = %s, business_scope = %s, update_at = now() WHERE company_id = %s;"
    print(updateDetailSql % updateDetailVal)
    company = mycursor.execute(updateDetailSql, updateDetailVal)
else:
    insertVal = (json_data["businessRegistration"]["socialCreditCode"], json_data["companyName"], json_data["companyPhone"],
                 json_data["companyEmail"], json_data["officialWebsite"], json_data["companyAddress"], json_data["companyProfile"],)
    insertSql = "INSERT INTO company (social_credit_code, company_name, company_phone, company_email, official_website, company_address, company_profile) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    print(insertSql % insertVal)
    company = mycursor.execute(insertSql, insertVal)
    # 最后插入行的主键id
    print(mycursor.lastrowid)
    companyRegistration = json_data["businessRegistration"]
    registeredCapital = companyRegistration["registeredCapital"].replace(
        "万(元)", "").replace(",", "")
    paidInCapital = companyRegistration["paidInCapital"]
    if '-' == paidInCapital:
        paidInCapital = None
    operatingPeriod = companyRegistration["operatingPeriod"]
    operatingPeriodList = operatingPeriod.split("至")
    operatingPeriodBegin = operatingPeriodList[0].strip()
    operatingPeriodEnd = operatingPeriodList[1].strip()
    insertDetailVal = (mycursor.lastrowid, companyRegistration["legalRepresentative"], companyRegistration["operatingStatus"], registeredCapital,
                       paidInCapital, companyRegistration["industry"], companyRegistration[
                           "socialCreditCode"], companyRegistration["taxpayerIdentificationNumber"],
                       companyRegistration["businessRegistrationNumber"], companyRegistration[
                           "organizationCode"], companyRegistration["registrationAuthority"],
                       companyRegistration["establishmentDate"], companyRegistration[
                           "enterpriseType"], operatingPeriodBegin, operatingPeriodEnd,
                       companyRegistration["administrativeDivisions"], companyRegistration[
                           "annualInspectionDate"], companyRegistration["registeredAddress"],
                       companyRegistration["businessScope"])
    insertDetailSql = "INSERT INTO company_registration (company_id, legal_representative, operating_status, registered_capital, paidIn_capital, industry, social_credit_code, taxpayer_identification_number, company_registration_number, organization_code, registration_authority, establishment_date, enterprise_type, operating_period_begin, operating_period_end, administrative_divisions, annualInspection_date, registered_address, business_scope) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    print(insertDetailSql % insertDetailVal)
    company = mycursor.execute(insertDetailSql, insertDetailVal)
con.commit()
