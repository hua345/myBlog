import pandas
from string import Template

jsonFile = "data.json"

df = pandas.read_json(jsonFile)
df.sort_values(['bookName','id'],ascending=[1,0],inplace=True)
grouped = df.groupby(['bookName']).head(1)
dictData = grouped.to_dict(orient="records")

hellpTemplate = Template('hello \'$name\' \'$id\' \n')

with open ('result.sql','w+') as f: 
    for rowDict in dictData:
        resultStr = hellpTemplate.safe_substitute(name=rowDict["bookName"],id=rowDict["id"])
        f.write(resultStr)

