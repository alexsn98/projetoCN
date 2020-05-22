#!flask/bin/python
import psycopg2
import psycopg2.extras
import pandas as pd

db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
        host='127.0.0.1', port='5431')

cur = db.cursor()

get_country_query = "SELECT CountryCode, year, Value FROM indicators WHERE indicatorcode =(%s) ORDER BY CountryCode;"

data = ("EN.ATM.CO2E.PC", )

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

  if currentCountry == "":
    currentCountry = i[0]
    countryYears = []

  if currentCountry != i[0]:
    notInYear = [y for y in years if y not in countryYears] #(╯°□°）╯︵ ┻━┻

    for y in notInYear:
      dataset[y].append(0)
    
    currentCountry = i[0]
    countryYears = []

  dataset[yearEntry].append(float(i[2]))
  countryYears.append(yearEntry)

notInYear = [y for y in years if y not in countryYears]

for y in notInYear:
  dataset[y].append(0)

#1963

#   years.append(i[0])
#   values.append(i[1])

# dataset['year'] = years
# dataset['value'] = values

df = pd.DataFrame(dataset)


# df.to_csv('ola.csv', index=False)