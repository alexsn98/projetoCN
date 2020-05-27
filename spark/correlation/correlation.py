#!/usr/bin/env python3
import psycopg2
import pandas as pd
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from google.cloud import storage

db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
          host='10.16.32.3', port='5432')

conn, cur = (db, db.cursor())

sc= SparkContext()

storage_client = storage.Client()
bucket_name = "project-files-cn"
bucket = storage_client.bucket(bucket_name)

source_file_name = "corr.csv"
destination_blob_name = "corr.csv"

#use cases FALTA ADICIONAR
use_cases = {}
use_cases["SP.DYN.LE00.IN"] = ["SL.GDP.PCAP.EM.KD","SN.ITK.DEFC.ZS","VC.IHR.PSRC.P5","SH.DYN.NMRT","SH.DTH.IMRT","SH.DYN.MORT"]

def get_data(country_code,use_case_target):
  use_case = use_cases[use_case_target]

  get_country_query = "SELECT i.CountryCode, i.indicatorCode, i.Value, i.year " \
    "FROM indicators i, country c WHERE c.CountryCode = i.CountryCode AND i.countryCode = ('" + country_code + "') " \
    "AND (i.indicatorcode='"+use_case_target+"' OR i.indicatorcode='"+use_case[0]+"' OR i.indicatorcode='"+use_case[1]+"' OR i.indicatorcode='"+use_case[2]+"' OR i.indicatorcode='"+use_case[3]+"' OR i.indicatorcode='"+use_case[4]+"' OR i.indicatorcode='"+use_case[5]+"') ORDER BY i.CountryCode;"

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
  target = target.replace('.', '-')
  sqlContext = SQLContext(sc)

  file_name_in_bucket = "gs://project-files-cn/"+ destination_blob_name

  df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(file_name_in_bucket)

  correlation_results = []

  for i in df.columns:
    corr_value = df.stat.corr(target,i)
    if (corr_value != 1):
      correlation_results.append([i, round(corr_value, 4)])

  return correlation_results


def save_in_db(country, target, correlation_results):
  for corr_result in correlation_results:
    indicator_code = corr_result[0]
    correlation_value = corr_result[1]

    add_correlation_query = "INSERT INTO correlation_result (country, indicatorcode, targetcode, correlationvalue) VALUES ('"+country+"','"+indicator_code+"','"+target+"','"+str(correlation_value)+"');"
    cur.execute(add_correlation_query)

  conn.commit()

if __name__ == "__main__":
  for target in use_cases.keys():
    get_countries_query = "SELECT DISTINCT c.CountryCode FROM country c, indicators i WHERE c.region='Europe & Central Asia'AND " \
     "c.CountryCode = i.CountryCode AND i.indicatorcode = '"+target+"';"

    cur.execute(get_countries_query)
    countries = list(map(lambda x: x[0],cur.fetchall()))

    for country in countries:
      destination_blob_name = country + "_" + target.replace('.', '-') + "_corr.csv"

      db_data = get_data(country,target)
      build_csv_file(db_data)
      correlation_results = get_correlation(target)
      save_in_db(country, target, correlation_results)