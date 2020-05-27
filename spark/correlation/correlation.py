#!/usr/bin/env python3
import psycopg2
import pandas as pd
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from google.cloud import storage

storage_client = storage.Client()
bucket_name = "project-files-cn"
bucket = storage_client.bucket(bucket_name)

source_file_name = "corr.csv"
destination_blob_name = "corr.csv"

def get_data(country):
  db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
            host='10.16.32.3', port='5432')
  cur = db.cursor()

  get_country_query = "SELECT i.CountryCode, i.indicatorCode, i.Value, i.year " \
    "FROM indicators i, country c WHERE c.CountryCode = i.CountryCode AND i.countryCode = ('" + country + "') ORDER BY i.CountryCode;"

  cur.execute(get_country_query)
  return cur.fetchall()

def build_csv_file(result):
  query_indicators = list(set([row[1] for row in result]))
  indicators = list(map(lambda ind : ind.replace(".","-"), query_indicators))
  dataset = {}

  for ind in indicators:
    dataset[ind] = []

  currentYear = ""

  for row in result:
    indicatorCode = row[1].replace('.', '-') 

    if currentYear == "":
      currentYear = row[3]
      yearIndicators = []

    if currentYear != row[3]: #fill with zeros
      notInIndicators = [ind for ind in indicators if ind not in yearIndicators] 

      for ind in notInIndicators:
        dataset[ind].append(0)
      
      currentYear = row[3]
      yearIndicators = []

    dataset[indicatorCode].append(float(row[2]))
    yearIndicators.append(indicatorCode)

  notInIndicators = [ind for ind in indicators if ind not in yearIndicators] 

  for ind in notInIndicators:
    dataset[ind].append(0)

  df = pd.DataFrame(dataset)

  blob = bucket.blob(destination_blob_name)
  
  df.to_csv(source_file_name, index=False)
  blob.upload_from_filename(source_file_name)


def get_correlation(target):
  sc= SparkContext()
  sqlContext = SQLContext(sc)

  # source_blob_name = "corr.csv"
  # destination_file_name = "corr.csv"
  
  # blob = bucket.blob(source_blob_name)
  # blob.download_to_filename(destination_file_name)

  file_name_in_bucket = "gs://project-files-cn/"+ destination_blob_name

  df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(file_name_in_bucket)

  print(df)

  minimum = 0.8
  correlation_results = []

  for i in df.columns:
    corr_value = df.stat.corr(target,i)
    if (corr_value >= minimum and corr_value != 1):
      correlation_results.append([i, corr_value])

  return correlation_results


def save_in_db(country, target, correlation_results):
  db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
            host='10.16.32.3', port='5432')

  conn, cur = (db, db.cursor())

  for corr_result in correlation_results:
    indicator_code = corr_result[0]
    correlation_value = corr_result[1]
    add_correlation_query = "INSERT INTO correlation_result (country, indicatorcode, targetcode, correlationvalue) VALUES ('"+country+"','"+indicator_code+"','"+target+"','"+str(correlation_value)+"');"
    cur.execute(add_correlation_query)

  conn.commit()

if __name__ == "__main__":
  # db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
  #           host='10.16.32.3', port='5432')

  # cur = db.cursor()
  # get_countries_query = "SELECT DISTINCT CountryCode FROM indicators;"

  # cur.execute(get_countries_query)
  # countries = list(map(lambda x: x[0],cur.fetchall()))

  # for country in countries:
  #   get_country_indicators_query = "SELECT DISTINCT indicatorcode FROM indicators WHERE countrycode = ('"+ country +"');"

  #   cur.execute(get_country_indicators_query)
  #   indicators = list(map(lambda x: x[0],cur.fetchall()))

  #   for indicator in indicators:

  country = "PRT"
  indicator = "EN.ATM.CO2E.EG.ZS"
  destination_blob_name = country + "_" + indicator + "_corr.csv"

  indicator = indicator.replace('.', '-')

  db_data = get_data(country)

  build_csv_file(db_data)

  correlation_results = get_correlation(indicator)

  save_in_db(country, indicator, correlation_results)