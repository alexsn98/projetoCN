import psycopg2
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression 

def get_from_db(indicator_code, region):
  db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
          host='127.0.0.1', port='5431')
  cur = db.cursor()

  get_country_query = "SELECT i.year, i.indicatorCode ,i.Value " \
    "FROM indicators i, country c WHERE c.Region ='Europe & Central Asia' AND c.CountryCode = i.CountryCode AND" \
    "(i.indicatorCode='NY.GDP.PCAP.KD' OR i.indicatorCode='EN.ATM.CO2E.PC' OR i.indicatorCode='SI.POV.2DAY' OR i.indicatorCode='SI.POV.2DAY' " \
    ") ORDER BY i.year;" 

  cur.execute(get_country_query)

  return cur.fetchall()


def create_csv_file(result, file_name):
  dataset = {}

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
      notInYear = [y for y in years if y not in countryYears] 

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


def train_regression(file_name):
  spark = SparkSession.builder.getOrCreate() 

  data = spark.read.csv(file_name, header=True, inferSchema=True)

  feature_columns = data.columns[1:-1]
  lastYear = data.columns[-1]

  assembler = VectorAssembler(inputCols=feature_columns, outputCol="features") 

  data_2 = assembler.transform(data) 
  # train, test = data_2.randomSplit([0.8, 0.2])

  algo = LinearRegression(featuresCol="features", labelCol=lastYear) 
  model = algo.fit(data_2) 

  predictions = model.transform(data_2)
  predictions.select(["countries","2012", "2013", "prediction"]).show()

  return model

def save_in_db():
  pass

if __name__ == "__main__":
  #regions = ['East Asia & Pacific'],'Middle East & North Africa','Latin America & Caribbean','','North America','Sub-Saharan Africa','South Asia']  
  indicator_code = ""

  for region in regions:
    file_name = indicator_code + "_" + region + ".csv"

    data = get_from_db(indicator_code, region)
    create_csv_file(data, file_name)

    # linearRegression.train_regression(file_name)