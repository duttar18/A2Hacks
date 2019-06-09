from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lxml import html, etree
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests, json
from operator import itemgetter
import cherrypy


class Aggregator(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getData(self,year,month,day,customString):
        custom = customString.split(",")
        
        page = requests.get("https://events.umich.edu/day/"+year+"-"+month+"-"+day+"?filter=all")
        tree = html.fromstring(page.content)

        pages = tree.xpath('//div[@class="event-info"]/h3/a/@href')

        data = []

        for page in pages:
            event_page = requests.get("https://events.umich.edu" + page)
            event_tree = html.fromstring(event_page.content)
            title = event_tree.xpath('//h1[@class="title"]/text()')[0].strip().replace(';','')
            description = event_tree.xpath('//div[@class="event-description"]/text()')[0].strip().replace(';','')
            location = event_tree.xpath('//div[@class="occurrences "]/h4/text()');
            location = [loc.strip() for loc in location];
            location = list(filter(lambda x: x != '', location));
            location = [' '.join(loc.split()) for loc in location];
            location = location[0] if location != [] else ' ';
            time = event_tree.xpath('//time/@datetime')[0].strip().replace(';','')
            cost = event_tree.xpath('//i[@class="fa fa-fw fa-money"]/../text()')[0].strip().replace(';','') if event_tree.xpath('//i[@class="fa fa-fw fa-money"]/../text()') else " "
            event_type = event_tree.xpath('//i[@class="fa fa-fw fa-list"]/../text()')[0].strip().replace(';','')
            tags = [tag.strip() for tag in event_tree.xpath('//i[@class="fa fa-fw fa-tags"]/../text()')]
            data.append(
                    {
                'Title': title,
                'Desc': description,
                'Loc': location,
                'Time': time,
                'Cost': cost,
                'Type': event_type,
                'Tags': tags  }
            )


        for x in data:
            imp  = 0
            for word in custom:
                if word in x['Title']:
                    imp+=5
                read = x['Desc'].split(" ");
                for part in read:
                    if word in part:
                        imp+=1
            x['Importance']=imp



        filtered = [x for x in data if x['Importance']>0]
        ranked = sorted(filtered, key = itemgetter('Importance'))
        return ranked
if __name__ == '__main__':
    cherrypy.quickstart(Aggregator())