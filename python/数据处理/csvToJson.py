import pandas
csvFile = "data.csv"

df = pandas.read_csv(csvFile)
json = df.to_json(orient="records",force_ascii=False)
print(df)
print(json)