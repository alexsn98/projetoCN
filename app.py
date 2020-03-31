#!flask/bin/python
from flask import Flask,jsonify
from markupsafe import escape
import connect_database as cd

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/country', methods=['GET'])
def get_all_countries():
    return "countries"

@app.route('/country/<countryCode>', methods=['GET'])
def get_country(countryCode):
    response = cd.get_country_from_db(countryCode)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)