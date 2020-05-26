import preProcessData
import linearRegression
import psycopg2
import sys
import pandas as pd

if __name__ == "__main__":
  regions = ['East Asia & Pacific'] #,'Middle East & North Africa','Latin America & Caribbean','Europe & Central Asia','North America','Sub-Saharan Africa','South Asia']  
  indicator_code = sys.argv[1]

  for region in regions:
    file_name = indicator_code + "&" + region + ".csv"

    data = preProcessData.get_from_db(indicator_code, region)

    print(data)

    # preProcessData.create_csv_file(data, file_name)

    # linearRegression.train_regression(file_name)