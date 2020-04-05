#!flask/bin/python
from flask import Flask, jsonify, make_response, g
import psycopg2
import psycopg2.extras

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

@app.route('/countries', methods=['GET'])
def get_all_countries():
    cur = g.db.cursor()

    get_all_countries_query = "SELECT * FROM country;"
    cur.execute(get_all_countries_query)

    query_result = cur.fetchall()
    
    del query_result[0] #remove column names

    if len(query_result) > 0:
        r = make_response(jsonify(query_result))
        r.status_code = 200

    else:
        r = make_response("Nenhum pais encontrado")
        r.status_code = 404
    
    return r


@app.route('/country/<countryCode>', methods=['GET'])
def get_country(countryCode):
    cur = g.db.cursor()

    get_country_query = "SELECT * FROM country WHERE countrycode=(%s);"
    data = (countryCode, )
    cur.execute(get_country_query, data)
    
    query_result = cur.fetchone()

    if query_result is not None:
        r = make_response(query_result)
        r.status_code = 200

    else:
        r = make_response("Nenhum pais encontrado")
        r.status_code = 404
    
    return r

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 