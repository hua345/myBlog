import mysql.connector

config = {
    'user': 'root',
    'password': 'xxx',
    'host': '192.168.137.129',
    'port': '3306',
    'database': 'db_example'
}

class MySQLPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = mysql.connector.connect(**config)
        # 通过cursor执行增删查改
        self.mycursor = self.connect.cursor()

    def process_item(self, item, spider):
        val = (item["businessRegistration"]["socialCreditCode"],)
        sql = "SELECT * FROM company where social_credit_code = %s "
        print(sql % val)
        self.mycursor.execute(sql, val)
        data = self.mycursor.fetchone()  # fetchone() 获取一条记录
        if data:
            print(data)
            updateVal = (item["companyName"], item["companyPhone"],
                        item["companyEmail"], item["officialWebsite"], item["companyAddress"], item["companyProfile"], data[0])
            updateSql = "UPDATE company SET company_name = %s, company_phone = %s, company_email = %s, official_website = %s, company_address = %s, company_profile = %s,update_at = now() WHERE id = %s ;"
            print(updateSql % updateVal)
            self.mycursor.execute(updateSql, updateVal)
            companyRegistration = item["businessRegistration"]
            registeredCapital = companyRegistration["registeredCapital"].replace(",", "")
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
            self.mycursor.execute(updateDetailSql, updateDetailVal)
        else:
            insertVal = (item["businessRegistration"]["socialCreditCode"], item["companyName"], item["companyPhone"],
                        item["companyEmail"], item["officialWebsite"], item["companyAddress"], item["companyProfile"],)
            insertSql = "INSERT INTO company (social_credit_code, company_name, company_phone, company_email, official_website, company_address, company_profile) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            print(insertSql % insertVal)
            self.mycursor.execute(insertSql, insertVal)
            # 最后插入行的主键id
            print(self.mycursor.lastrowid)
            companyRegistration = item["businessRegistration"]
            registeredCapital = companyRegistration["registeredCapital"].replace(",", "")
            paidInCapital = companyRegistration["paidInCapital"]
            if '-' == paidInCapital:
                paidInCapital = None
            operatingPeriod = companyRegistration["operatingPeriod"]
            operatingPeriodList = operatingPeriod.split("至")
            operatingPeriodBegin = operatingPeriodList[0].strip()
            operatingPeriodEnd = operatingPeriodList[1].strip()
            insertDetailVal = (self.mycursor.lastrowid, companyRegistration["legalRepresentative"], companyRegistration["operatingStatus"], registeredCapital,
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
            self.mycursor.execute(insertDetailSql, insertDetailVal)
        self.connect.commit()
        return item  # 必须实现返回