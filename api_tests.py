'''
  api_tests.py
  Authors: Aman Panda, Abha Laddha, Noah Brackenbury 
  9 February 2017
'''

# Import necessary packages
import unittest
import api
import flask

"""
Class that contains our tests for api.py
"""
class api_tests(unittest.TestCase):

  """
  Given a country we should get the list of all emissions across the years of that country. 
  Here the country is India and we are checking the first array element which returns the data 
  for year 1990. 
  """
  def test_country(self):
      self.assertEqual(api._searchCountry("India")[0], ("IND", "India", "total", 690577.0, 737852.0, 783634.0, 814298.0, 864932.0, 920047.0, 1002220.0, 1043940.0, 
        1071910.0, 1144390.0, 1186660.0, 1203840.0, 1226790.0, 1281910.0, 1346600.0, 1411130.0, 1504360.0, 1612380.0, 1742700.0))

  """
  Given a country we should get the list of all emissions across the years of that country. 
  Here the country is invalid, so we should get an empty list.
  """
  def test_wrongCountry(self):
      self.assertEqual(api._searchCountry("feif"),[])

  """
  Given the year and kind of CO2 emissions, we should get the list of all countries. 
  Here we are checking the first element of our return array with what should be returned. 
  """
  def test_WorldTotal(self):
      self.assertEqual(api._getWorldData("y1992", "total")[0], ("Aruba", 1723.49))

  """
  Given the year and kind of CO2 emissions, we should get the list of all countries. 
  Here we are checking the first element of our return array with what should be returned. 
  """
  def test_WorldGDP(self):
      self.assertEqual(api._getWorldData("y2008", "GDP")[0], ("Aruba", 0))

  """
  Given the year and kind of CO2 emissions, we should get the list of all countries. 
  Here we are checking the first element of our return array with what should be returned. 
  """
  def test_WorldCapita(self):
      self.assertEqual(api._getWorldData("y2007", "capita")[0], ("Aruba", 22.62))

if __name__ == '__main__':
    unittest.main()
