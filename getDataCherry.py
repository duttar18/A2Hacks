from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lxml import html, etree
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests, json
from operator import itemgetter
import cherrypy


import scraper


class Aggregator(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getData(self,year,month,day,customString):
        custom = customString.split(",")
        
        

        with open('data_file.json', 'r') as dataFile:
            dataReader=dataFile.read()

        dataAllDays = json.loads(dataReader)

        data=dataAllDays[year+"-"+month+"-"+day]

        for x in data:
            imp  = 0
            for word in custom:
                rea = x['Title'].split(" ")
                for part in rea:
                    if word.lower()==part.lower():
                        imp+=5
                read = x['Desc'].split(" ")
                for part in read:
                    if word.lower()==part.lower():
                        imp+=1
                for part in x['Tags']:
                    if word.lower()==part.lower():
                        imp+=5
            x['Importance']=imp



        filtered = [x for x in data if x['Importance']>0]
        ranked = sorted(filtered, key = itemgetter('Importance'))
        return ranked
if __name__ == '__main__':
    cherrypy.quickstart(Aggregator())