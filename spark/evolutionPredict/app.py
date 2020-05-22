#!flask/bin/python
from flask import Flask, jsonify, make_response, g, request
import psycopg2
from psycopg2.extras import RealDictCursor
import re

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(dbname='postgres', user='postgres', password='CNgrupo8',
            host='127.0.0.1', port='5432', cursor_factory=RealDictCursor)
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

@app.route('/spark/evolutionPredict/<countryCode>/<indicatorCode>', methods=['GET'])
def get_evolution(countryCode, indicatorCode):
    cur = g.db.cursor()

    get_evolution_query = "SELECT * FROM evolution WHERE countrycode=(%s) AND indicatorcode=(%s);"
    data = (countryCode, indicatorCode)
    cur.execute(get_evolution_query, data)
    
    query_result = cur.fetchone()

    if query_result is not None:
        r = make_response(query_result)
        r.status_code = 200

    else: 
        r = make_response("Country or Indicator not found")
        r.status_code = 404

    return r

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 