#!flask/bin/python
from flask import Flask, jsonify, make_response, g
from markupsafe import escape
import psycopg2

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(
            host='10.16.32.3', port='5432')
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def hello():
    return "Hello world!"

@app.route('/countries', methods=['GET'])
def get_all_countries():
    conn, cur = (g.db, g.db.cursor())

    get_all_countries_query = "SELECT * FROM country;"
    cur.execute(get_all_countries_query)
    query_result = cur.fetchall()

    del query_result[0] #remove column names

    countries = []
    
    for country in query_result:
        countries.append(create_country(list(country))) #create country json objet

    r_countries = countries

    r = make_response(jsonify(r_countries))
    r.status_code = 200
    
    return r


@app.route('/country/<countryCode>', methods=['GET'])
def get_country(countryCode):
    conn, cur = (g.db, g.db.cursor())

    get_country_query = "SELECT * FROM country WHERE countrycode=(%s);"
    data = (countryCode, )
    cur.execute(get_country_query, data)
    
    query_result = cur.fetchone()

    r_country = create_country(list(query_result)) #create country json objet

    r = make_response(jsonify(r_country))
    r.status_code = 200
    
    return r

def create_country(country):
    country_json = {}
    country_json['shortname'] = country[1]
    country_json['longname'] = country[2]
    country_json['currencyunit'] = country[3]
    country_json['region'] = country[4]
    country_json['incomegroup'] = country[5]
    country_json['latestpopulationcensus'] = country[6]
    country_json['latesthouseholdsurvey'] = country[7]
    country_json['latestagriculturalcensusentry'] = country[8]
    country_json['latestindustrialdata'] = country[9]
    country_json['latesttradedata'] = country[10]

    return country_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 