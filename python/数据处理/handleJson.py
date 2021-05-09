import pandas
from string import Template

jsonFile = "data.json"

df = pandas.read_json(jsonFile)
dictData = df.to_dict(orient="records")
print(df)
print(dictData)

for row in df.itertuples():
    print(row.bookName)

hellpTemplate = Template('hello $name $world')

for rowDict in dictData:
    resultStr = hellpTemplate.safe_substitute(name=rowDict["bookName"])
    print(resultStr)

