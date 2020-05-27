#!/usr/bin/env python3
import psycopg2
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression 
from google.cloud import storage

db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
        host='10.16.32.3', port='5432')
conn, cur = (db, db.cursor())

features = ["EN-ATM-CO2E-PC","SH-XPD-PCAP-PP-KD","AG-LND-AGRI-ZS","SH-XPD-PCAP-PP-KD","SE-TER-ENRR","SI-POV-2DAY","SL-UEM-TOTL-NE-ZS"]
years = [1978,1971,1978,1971,1980,1968,2008,1988,1972,1996,2009,2003,1965,1976,1966,1985,2005,1990,1960,2000,2004,2006,2007,2010,2011]

storage_client = storage.Client()
bucket_name = "project-files-cn"
bucket = storage_client.bucket(bucket_name)

def get_train_from_db(year):
  get_country_query = "SELECT c.countrycode, i.indicatorCode ,i.Value FROM indicators i, country c WHERE c.CountryCode = i.CountryCode AND i.year='"+year+"' AND " \
    "(i.indicatorCode='NY.GDP.PCAP.KD' OR i.indicatorCode='EN.ATM.CO2E.PC' OR i.indicatorCode='SH.DTH.NCOM.ZS' OR i.indicatorCode='AG.LND.AGRI.ZS' " \
    "OR i.indicatorCode='SH.XPD.PCAP.PP.KD' OR i.indicatorCode='SE.TER.ENRR' OR i.indicatorCode='SI.POV.2DAY' " \
    "OR i.indicatorCode='SL.UEM.TOTL.NE.ZS') ORDER BY c.countrycode;" 
  cur.execute(get_country_query)

  return cur.fetchall()

def get_test_from_db(year):
  get_country_query = "SELECT c.countrycode, i.indicatorCode ,i.Value FROM indicators i, country c WHERE c.Region ='East Asia & Pacific' AND c.CountryCode = i.CountryCode AND i.year='"+year+"' AND " \
    "(i.indicatorCode='EN.ATM.CO2E.PC' OR i.indicatorCode='SH.DTH.NCOM.ZS' OR i.indicatorCode='AG.LND.AGRI.ZS' " \
    "OR i.indicatorCode='SH.XPD.PCAP.PP.KD' OR i.indicatorCode='SE.TER.ENRR' OR i.indicatorCode='SI.POV.2DAY' " \
    "OR i.indicatorCode='SL.UEM.TOTL.NE.ZS') ORDER BY c.countrycode;" 
  cur.execute(get_country_query)

  return cur.fetchall()


def build_model(result):
  dataset = {}
  dataset["countries"] = []
  indicators = set([i[1].replace(".", "-") for i in result])

  for indicator in indicators:
    dataset[indicator] = []

  currentCountry= ""

  for i in result:
    indicatorEntry = i[1].replace(".", "-")

    if currentCountry == "": #first iteration
      currentCountry = i[0]
      dataset["countries"].append(currentCountry)
      yearIndicators = []

    if currentCountry != i[0]: #fill with zeros
      notInIndicator = [ind for ind in indicators if ind not in yearIndicators] 
      for ind in notInIndicator:
        dataset[ind].append(0)
      
      currentCountry = i[0]
      dataset["countries"].append(currentCountry)
      yearIndicators = []

    dataset[indicatorEntry].append(float(i[2]))
    yearIndicators.append(indicatorEntry)

  notInIndicator = [ind for ind in indicators if ind not in yearIndicators] 
  for ind in notInIndicator:
    dataset[ind].append(0)

  # Fill missing values with average
  for ind in indicators:
    average = np.average(dataset[ind])
    dataset[ind] = [average if value == 0 else value for value in dataset[ind]]

  df = pd.DataFrame(dataset)

  cols = df.columns.tolist() #put countries as first column
  cols = cols[-1:] + cols[:-1]
  df = df[cols]

  return df


def train_regression(file_name):
  spark = SparkSession.builder.getOrCreate() 
  data = spark.read.csv("gs://project-files-cn/"+file_name, header=True, inferSchema=True)

  assembler = VectorAssembler(inputCols=features, outputCol="features") 
  data_2 = assembler.transform(data) 

  algo = LinearRegression(featuresCol="features", labelCol="NY-GDP-PCAP-KD") 
  model = algo.fit(data_2) 

  return model

def predict(model, file_name):
  spark = SparkSession.builder.getOrCreate() 
  data = spark.read.csv("gs://project-files-cn/"+file_name, header=True, inferSchema=True)

  assembler = VectorAssembler(inputCols=features, outputCol="features") 
  data_2 = assembler.transform(data) 

  predictions = model.transform(data_2)

  return predictions

def save_in_db():
  for year in years:
    if year >= 2004:
      test_data = get_test_from_db(str(year))
      test_dataframe = build_model(test_data)

      blob = bucket.blob("test.csv")
      test_dataframe.to_csv("test.csv", index=False)
      blob.upload_from_filename("test.csv")
      
      prediction = predict(model, "test.csv")

      prediction_results = prediction.rdd.map(lambda x: (x.countries, x.prediction))

      for p in prediction_results.toLocalIterator():
        add_correlation_query = "INSERT INTO regression_result (country, indicator, prediction, year) VALUES ('"+p[0]+"','NY-GDP-PCAP-KD','"+str(p[1])+"','"+str(year)+"');"
        cur.execute(add_correlation_query)

      conn.commit()

if __name__ == "__main__":
  dataframes_for_training = []

  #train
  for year in years:
    train_data = get_train_from_db(str(year))
    dataframes_for_training.append(build_model(train_data))

  train_dataframe = pd.concat(dataframes_for_training)

  average_to_replace = {
    "EN-ATM-CO2E-PC": train_dataframe["EN-ATM-CO2E-PC"].mean(),
    "SH-XPD-PCAP-PP-KD": train_dataframe["SH-XPD-PCAP-PP-KD"].mean(),
    "AG-LND-AGRI-ZS": train_dataframe["AG-LND-AGRI-ZS"].mean(),
    "SE-TER-ENRR": train_dataframe["SE-TER-ENRR"].mean(),
    "SI-POV-2DAY": train_dataframe["SI-POV-2DAY"].mean(),
    "SL-UEM-TOTL-NE-ZS": train_dataframe["SL-UEM-TOTL-NE-ZS"].mean(),
  }

  train_dataframe = train_dataframe.fillna(value=average_to_replace)

  blob = bucket.blob("train.csv")
  train_dataframe.to_csv("train.csv", index=False)
  blob.upload_from_filename("train.csv")

  model = train_regression("train.csv")

  #test
  save_in_db()