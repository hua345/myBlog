import pandas
jsonFile = "data.json"

df = pandas.read_json(jsonFile)
dictData = df.to_dict(orient="records")
print(df)
print(dictData)

for row in df.itertuples():
    print(row.bookName)

for rowDict in dictData:
    print(rowDict)
