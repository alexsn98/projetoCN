#!flask/bin/python3
from flask import Flask, jsonify, make_response, g
import psycopg2
import psycopg2.extras
import re

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello world!"

@app.route('/correlation/<string:country_id>/<string:case>', methods=['GET'])
def get_indicator_correlation(country_id, case):
    db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
        host='127.0.0.1', port='5432')

    cur = db.cursor()

    if re.search("[A-Z]{3}", country_id): #valid country code
        
        get_correlation_query = "SELECT * FROM correlation_result WHERE country=(%s) AND targetcode=(%s);"

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

        query_result_formated = []

        for row in query_result:
            row_dict = {}
            row_dict["country"] = row[0]
            row_dict["indicatorcode"] = row[1]
            row_dict["targetcode"] = row[2]
            row_dict["correlationvalue"] = str(row[3])

            query_result_formated.append(row_dict)

        if query_result is not None: #country exists
            r = make_response(jsonify(query_result_formated))
            r.status_code = 200

        else: 
            r = make_response("Correlation not found")
            r.status_code = 404
    else:
        r = make_response("Invalid country code supplied")
        r.status_code = 400

    db.close()

    return r

@app.route('/regression/<string:country_id>/<string:year>', methods=['GET'])
def get_indicator_regression(country_id, year):
    db = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
        host='127.0.0.1', port='5432', cursor_factory=psycopg2.extras.RealDictCursor)

    cur = db.cursor()

    #falta verificar indicador code
    if re.search("[A-Z]{3}", country_id): #valid country code
        if (int(year) >= 2004 and int(year) <= 2014): #valid indicator code
            get_regression_query = "SELECT * FROM regression_result WHERE country=(%s) AND year=(%s);"
            data = (country_id, year, )
            cur.execute(get_regression_query, data)
            
            query_result = cur.fetchall()

            if query_result is not None: #country exists
                r = make_response(jsonify(query_result))
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

    db.close()

    return r

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 