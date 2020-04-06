#!flask/bin/python
from flask import Flask, jsonify, make_response, g, request
import psycopg2
from psycopg2.extras import RealDictCursor

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

@app.route('/indicator', methods=['POST'])
def add_indicator():
    conn, cur = (g.db, g.db.cursor())

    request_data = request.get_json()

    add_indicator_query = "INSERT INTO indicators (countryname, countrycode, indicatorname, indicatorcode, year, value) VALUES (%s, %s, %s, %s, %s, %s);"

    data = (request_data['countryname'], request_data['countrycode'], request_data['indicatorname'], 
    request_data['indicatorcode'], request_data['year'], request_data['value'], )

    cur.execute(add_indicator_query, data)
    conn.commit()

    return "tudo bem"


@app.route('/indicator/<countryCode>', methods=['GET'])
def get_indicator(countryCode):
    cur = g.db.cursor()

    get_indicator_query = "SELECT * FROM indicators WHERE countrycode=(%s);"
    data = (countryCode, )
    cur.execute(get_indicator_query, data)
    
    query_result = cur.fetchall()

    if query_result is not None:
        r = make_response(jsonify(query_result))
        r.status_code = 200

    else:
        r = make_response("Nenhum indicator encontrado")
        r.status_code = 404
    
    return r

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 