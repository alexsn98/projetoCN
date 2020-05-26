import psycopg2
import correlation

if __name__ == "__main__":
  file_name = "corr.csv"

  db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
            host='127.0.0.1', port='5432')

  cur = db.cursor()
  get_countries_query = "SELECT DISTINCT CountryCode FROM indicators;"

  cur.execute(get_countries_query)
  countries = cur.fetchall()

  for country in countries:
    get_country_indicators_query = "SELECT DISTINCT indicator FROM indicators WHERE countrycode = (%s);"
    data = (country, )

    cur.execute(get_country_indicators_query)
    indicators = cur.fetchall()

    for indicator in indicators:
      indicator = indicator.replace('.', '-')

      db_data = correlation.get_data(country)

      correlation.build_csv_file(file_name, db_data)

      correlation_results = correlation.get_correlation(file_name, indicator)

      correlation.save_in_db(country, indicator, correlation_results)