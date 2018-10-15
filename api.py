'''
  api.py
  Authors: Aman Panda, Abha Laddha, Noah Brackenbury 
  16 February 2017
	Based upon code provided by Prof. Eric Alexander, January 2017
'''

# Import necessary packages
import flask
from flask import render_template, request, jsonify
import json
import sys
import psycopg2
import psqlConfig as config

app = flask.Flask(__name__)
#app.config['DEBUG'] = True

validCols = ['y1990','y1991', 'y1992', 'y1993', 'y1994', 'y1995', 'y1996', \
             'y1997', 'y1998', 'y1999', 'y2000', 'y2001', 'y2002', \
             'y2003', 'y2004', 'y2005', 'y2006', 'y2007', 'y2008']

"""
Function that defines the front page of the app. Returns
html for the front page.
"""
@app.route('/')
def frontPage():
    return render_template('frontpage.html')

"""
Function that defines the country page of the app. Returns
html for the country page.
"""
@app.route('/country/<countryName>')
def countryPageLoad(countryName):
  return render_template('country.html', countryName=countryName)

"""
Function that returns 3 lists for an input country, each list corresponding
to data for total, capita, and GDP for a given country, for all years in our
database.
Takes in an input String for country: e.g. "Australia", "India", etc.
Note that the first letter of the country must be capitalized at this point.
Calls the helper function _searchCountry()
"""
@app.route('/<countryName>')
def searchCountry(countryName):
  # In case the country is invalid, return empty array
  # Returns CO2 emissions for a country across total, per capita, and per GDP unit
  return jsonify({'rows': _searchCountry(countryName)})

# Helper function for searchCountry()
def _searchCountry(countryName):
  try:
    connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
  except Exception as e:
    print(e)
    exit()
  try:
    cursor =  connection.cursor()
    queryTemp = "SELECT * FROM climatechange WHERE country_name LIKE '%%' || %s || '%%'"
    cursor.execute(queryTemp, (countryName,))
  except Exception as e:
    print('Cursor error: {}'.format(e))
    connection.close()
    exit()
  rows = []
  for row in cursor:
    rows.append(row)
  connection.close()
  return rows

"""
Function that returns global CO2 emissions for a certain year in lists where each list
corresponds to data for some country.
Each tuple in the list that is returned is of the following form:
(String country, Real type_of_data_for_selected_year). Note that the latter parameter 
will correspond to whichever radio button that has been selected by the user.
Note that year has to be of the following form: "y1990", or "y1991",..., or "y2007", or "y2008"
and typeData must be of the following form: "total", or "GDP", or "capita".
Calls helper function _getWorldData()
"""
@app.route('/<year>/<typeData>')
def getWorldData(year, typeData):
  # Returns CO2 emissions across one of: total, per capita, and per GDP unit, for all countries of the world
  # e.g. for 1998 & CO2 total, [(Aruba, 1668.49), (Andorra, 484.04), (Afghanistan, 1056.1), (Angola, 7308.33)... etc.]
  return jsonify({'rows': _getWorldData(year, typeData)})


# Helper function for getWorldData()
def _getWorldData(year, typeData):
  try:
    connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
  except Exception as e:
    print(e)
    exit()
  try:
    cursor =  connection.cursor()
    queryTemp = "SELECT country_name, {} FROM climatechange WHERE co2_emissions =%s"
    if year in validCols:
      queryTemp = queryTemp.format(year)
    cursor.execute(queryTemp, (typeData,))
  except Exception as e:
    print('Cursor error: {}'.format(e))
    connection.close()
    exit()
  rows = []
  for row in cursor:
    rows.append(row)
  connection.close()
  return rows


# Main function
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
