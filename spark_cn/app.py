#!flask/bin/python
from flask import Flask, jsonify, make_response, g
import psycopg2
import psycopg2.extras
import re

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
        host='127.0.0.1', port='5432', cursor_factory=psycopg2.extras.RealDictCursor)
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

@app.route('/correlation/<string:country_id>/<string:case>', methods=['GET'])
def get_indicator_correlation(country_id, case):
    cur = g.db.cursor()

    if re.search("[A-Z]{3}", country_id): #valid country code
        
        get_correlation_query = "SELECT * FROM correlation_result WHERE countrycode=(%s) AND targetcode=(%s);"

        if(case == "case1"):
            data = (country_id, "EN.ATM.CO2E.PC", )
        elif(case == "case2"):
            data = (country_id, "SP.DYN.LE00.IN", )
        elif(case == "case3"):
            data = (country_id, "SE.ADT.LITR.ZS", ) #preencher o ultimo caso
        else:
            r = make_response("No such case found")
            r.status_code = 404
            return r
        
        cur.execute(get_correlation_query, data)
            
        query_result = cur.fetchall()

        if query_result is not None: #country exists
            r = make_response(query_result)
            r.status_code = 200

        else: 
            r = make_response("Correlation not found")
            r.status_code = 404
    else:
        r = make_response("Invalid country code supplied")
        r.status_code = 400

    return 0

@app.route('/regression/<string:country_id>/<string:year>', methods=['GET'])
def get_indicator_regression(country_id, year):
    cur = g.db.cursor()

    #falta verificar indicador code
    if re.search("[A-Z]{3}", country_id): #valid country code
        if (year >= 2011 & year <= 2014): #valid indicator code

            get_regression_query = "SELECT * FROM regression_result WHERE countrycode=(%s) AND year=(%s);"
            data = (country_id, year, )
            cur.execute(get_regression_query, data)
            
            query_result = cur.fetchall()

            if query_result is not None: #country exists
                r = make_response(query_result)
                r.status_code = 200

            else: 
                r = make_response("Correlation not found")
                r.status_code = 404
        else:
            r = make_response("Invalid year supplied")
            r.status_code = 400
    else:
        r = make_response("Invalid country code supplied")
        r.status_code = 400

    return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 