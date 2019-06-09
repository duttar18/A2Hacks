import json
from operator import itemgetter
import cherrypy
from lxml import html
import requests, json

def scrape():
    print("scraping")
    data = {}

    page = requests.get("https://events.umich.edu/week?filter=all")
    tree = html.fromstring(page.content)

    pages = tree.xpath('//div[@class="event-info"]/h3/a/@href')


    for page in pages:
        event_page = requests.get("https://events.umich.edu" + page)
        event_tree = html.fromstring(event_page.content)
        title = event_tree.xpath('//h1[@class="title"]/text()')[0].strip().replace(';','')
        description = event_tree.xpath('//div[@class="event-description"]/text()')[0].strip().replace(';','')
        location = event_tree.xpath('//div[@class="occurrences "]/h4/text()');
        location = [loc.strip() for loc in location]
        location = list(filter(lambda x: x != '', location))
        location = [' '.join(loc.split()) for loc in location]
        location = location[0] if location != [] else ' '
        time = event_tree.xpath('//time/@datetime')[0].strip().replace(';','')
        cost = event_tree.xpath('//i[@class="fa fa-fw fa-money"]/../text()')[0].strip().replace(';','') if event_tree.xpath('//i[@class="fa fa-fw fa-money"]/../text()') else " "
        event_type = event_tree.xpath('//i[@class="fa fa-fw fa-list"]/../text()')[0].strip().replace(';','')
        tags = [tag.strip() for tag in event_tree.xpath('//i[@class="fa fa-fw fa-tags"]/../text()')]
        data.setdefault(time.split(" ")[0],[]).append(
                {
            'Title': title,
            'Desc': description,
            'Loc': location,
            'Time': time,
            'Cost': cost,
            'Type': event_type,
            'Tags': tags  }
        )   
    with open("AAData.json") as read_file:
        aadata = json.load(read_file)
        for datum in aadata:
            data.setdefault(datum['Time'].split(" ")[0],[]).append({
            'Title': datum['Title'],
            'Desc': datum['Desc'],
            'Loc': datum['Loc'],
            'Time': datum['Time']
            })
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)

class Aggregator(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getData(self,year,month,day,customString):
        custom = customString.split(",")
        with open('data_file_with_coords.json', 'r') as dataFile:
            dataReader=dataFile.read()
        dataAllDays = json.loads(dataReader)
        data=dataAllDays.get(year+"-"+month+"-"+day,[])  
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
                for part in x.get('Tags',[]):
                    if word.lower()==part.lower():
                        imp+=5
            x['Importance']=imp
        filtered = [x for x in data if x['Importance']>0]
        ranked = sorted(filtered, key = itemgetter('Importance'))
        return ranked
if __name__ == '__main__':
    import sys
    import os
    port = os.environ['PORT']
    cherrypy.config.update({
                            'server.socket_host': '0.0.0.0',
                            'server.socket_port': int(port),
                           })
    cherrypy.response.headers['Content-Type'] = 'application/json'           
    cherrypy.quickstart(Aggregator())