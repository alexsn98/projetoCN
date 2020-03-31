import psycopg2

def get_country_from_db(country):
    conn = psycopg2.connect(user='postgres', password='CNgrupo8',
                        host='localhost', port='5431')
    cur = conn.cursor()

    SQL = "SELECT * FROM country WHERE countrycode=(%s);"
    data = (country, )
    cur.execute(SQL, data)
    
    result = cur.fetchone()

    toReturn = {"shortname": result[1],
            "longname": result[2],
            "currencyunit": result[3],
            "region": result[4],
            "incomegroup": result[5],
            "latestpopulationcensus": result[6],
            "lastesthouseholdsurvey": result[7],
            "latestindustrialdata": result[8],
            "latesttradedata": result[9],
    }

    cur.close()
    conn.close()    
    
    return(toReturn)