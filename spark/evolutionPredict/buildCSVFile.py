#!flask/bin/python
import psycopg2
import psycopg2.extras
import pandas as pd
import numpy as np

db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
        host='127.0.0.1', port='5431')

cur = db.cursor()

get_country_query = "SELECT CountryCode, year, Value FROM indicators WHERE indicatorcode =(%s) ORDER BY CountryCode;"

data = ("EN.ATM.CO2E.KT", )

cur.execute(get_country_query, data)

result = cur.fetchall()

dataset = {}
years = set([i[1] for i in result])
values = []

for year in years:
  dataset[year] = []

currentCountry = ""

for i in result:
  yearEntry = i[1]

  if currentCountry == "": #first iteration
    currentCountry = i[0]
    countryYears = []

  if currentCountry != i[0]: #fill with zeros
    notInYear = [y for y in years if y not in countryYears] #(╯°□°）╯︵ ┻━┻

    for y in notInYear:
      dataset[y].append(0)
    
    currentCountry = i[0]
    countryYears = []

  dataset[yearEntry].append(float(i[2]))
  countryYears.append(yearEntry)

notInYear = [y for y in years if y not in countryYears] #fill last zeros

for y in notInYear: 
  dataset[y].append(0) 

# Delete columns with missing values
# columns_to_delete = []   
# for column in dataset:
#   if 0 in dataset[column]:
#     columns_to_delete.append(column)

# for c in columns_to_delete:
#   del dataset[c]

# Fill missing values with average
# for column in dataset:
#   average = np.average(dataset[column])
  
#   dataset[column] = [average if value == 0 else value for value in dataset[column]]

# Fill missing values with median 
# for column in dataset:
#   median = np.median(dataset[column])
  
#   dataset[column] = [median if value == 0 else value for value in dataset[column]]


# Fill missing values with mode
for column in dataset:
  mode = max(set(dataset[column]), key=dataset[column].count)
  
  dataset[column] = [mode if value == 0 else value for value in dataset[column]]

df = pd.DataFrame(dataset)
df = df.reindex(sorted(df.columns), axis=1)

print(len(df.columns))

df.to_csv('indicators.csv', index=False)