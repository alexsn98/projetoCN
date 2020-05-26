import psycopg2
import pandas as pd
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

def get_data(country):
  db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
            host='127.0.0.1', port='5432')

  cur = db.cursor()

  get_country_query = "SELECT i.CountryCode, i.indicatorCode, i.Value, i.year " \
    "FROM indicators i, country c WHERE c.CountryCode = i.CountryCode AND i.countryCode = (%s) ORDER BY i.CountryCode;"

  data = (country, )

  cur.execute(get_country_query, data)

  return cur.fetchall()

def build_csv_file(file_name, result):
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
      notInIndicators = [ind for ind in indicators if ind not in yearIndicators] #(╯°□°）╯︵ ┻━┻

      for ind in notInIndicators:
        dataset[ind].append(0)
      
      currentYear = row[3]
      yearIndicators = []

    dataset[indicatorCode].append(float(row[2]))
    yearIndicators.append(indicatorCode)

  notInIndicators = [ind for ind in indicators if ind not in yearIndicators] #(╯°□°）╯︵ ┻━┻

  for ind in notInIndicators:
    dataset[ind].append(0)

  df = pd.DataFrame(dataset)

  df.to_csv(file_name, index=False)

def get_correlation(file_name, target):
  sc= SparkContext()
  sqlContext = SQLContext(sc)
  df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(file_name)

  minimum = 0.8
  correlation_results = []

  for i in df.columns:
    corr_value = df.stat.corr(target,i)
    if (corr_value >= minimum and corr_value != 1):
      correlation_results.append([i, corr_value])

  return correlation_results

def save_in_db(country, target, correlation_results):
  db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
            host='127.0.0.1', port='5432')

  conn, cur = (db, db.cursor())

  for corr_result in correlation_results:
    indicator_code = corr_result[0]
    correlation_value = corr_result[1]
    add_correlation_query = "INSERT INTO correlation_result (country, indicatorcode, targetcode, correlationvalue) VALUES (%s, %s, %s, %s);"

    data = (country, indicator_code, target, correlation_value)
    cur.execute(add_correlation_query, data)

  conn.commit()

  print("OK")