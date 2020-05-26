import psycopg2
import pandas as pd
import numpy as np

def get_from_db(indicator_code, region):
  db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
          host='127.0.0.1', port='5431')
  cur = db.cursor()

  get_country_query = "SELECT i.CountryCode, i.indicatorCode ,i.Value " \
    "FROM indicators i, country c WHERE c.Region =(%s) AND c.CountryCode = i.CountryCode AND" \
    "(i.indicatorCode='EN.ATM.CO2E.KT' OR i.indicatorCode='SP.DYN.CDRT.IN') ORDER BY i.CountryCode;"

  data = (region, )
  cur.execute(get_country_query, data)

  return cur.fetchall()

def create_csv_file(result, file_name):
  dataset = {}
  dataset['countries'] = []

  years = set([i[1] for i in result])

  for year in years:
    dataset[year] = []

  currentCountry = ""

  for i in result:
    yearEntry = i[1]

    if currentCountry == "": #first iteration
      currentCountry = i[0]
      dataset["countries"].append(currentCountry)
      countryYears = []

    if currentCountry != i[0]: #fill with zeros
      notInYear = [y for y in years if y not in countryYears] #(╯°□°）╯︵ ┻━┻

      for y in notInYear:
        dataset[y].append(0)
      
      currentCountry = i[0]
      dataset["countries"].append(currentCountry)
      countryYears = []

    dataset[yearEntry].append(float(i[2]))
    countryYears.append(yearEntry)

  notInYear = [y for y in years if y not in countryYears] #fill last zeros

  for y in notInYear: 
    dataset[y].append(0) 

  # Fill missing values with average
  for year in years:
    average = np.average(dataset[year])
    
    dataset[year] = [average if value == 0 else value for value in dataset[year]]

  df = pd.DataFrame(dataset)

  df = df.reindex(sorted(df.columns), axis=1)

  cols = df.columns.tolist() #put countries as first column
  cols = cols[-1:] + cols[:-1]

  df = df[cols]

  df.to_csv(file_name, index=False)