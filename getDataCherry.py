from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lxml import html, etree
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests, json
from operator import itemgetter
import cherrypy

import datetime

import scraper


class Aggregator(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getData(self,year,month,day,customString):
        custom = customString.split(",")
        
        
        with open('date.json', 'r') as timeFile:
            timeReader=timeFile.read()
        tim = json.loads(timeReader)

        if(tim!=datetime.datetime.today().day):
            scraper.scrape(year,month,day)
            print(tim)
            print(datetime.datetime.today().day)

        # read file
        with open('data_file.json', 'r') as dataFile:
            dataReader=dataFile.read()

        data = json.loads(dataReader)

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