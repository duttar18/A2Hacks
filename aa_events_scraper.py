from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lxml import html, etree
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import re
from dateutil import parser

browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
url = "https://www.visitannarbor.org/event?month=jun"
browser.get(url) #navigate to the page
myElem = WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, 'cardFront')))
print("got")
innerHTML = browser.execute_script("return document.body.innerHTML")
tree = html.fromstring(innerHTML)
cards = tree.xpath('//div[@class="cardContent"]')

data = []

for card in cards:
    card = html.tostring(card)
    card = html.fromstring(card) # Refocus
    title = card.xpath('//div[@class="cardFront"]//div/h3/a/text()')[0]
    description = card.xpath('//div[@class="cardBack"]//div[@class="desc"]/descendant-or-self::text()')
    time = description[2].replace('\\','').replace('/', '')
    description = description[0]
    date = card.xpath('//div[@class="cardFront"]//div[@class="times"]/div[@class="start"]/text()')[0]
    location = card.xpath('//div[@class="cardFront"]//div[@class="street"]/text()')[0]
    location = ' '.join(''.join(location).split())
    print(time)
    time = re.findall('\d\d:\d\d [pa]\.m\.|\d:\d\d [pa]\.m\.|\d [pa]\.m\.|\d\d [pa]\.m\.|\d\d:\d\d|\d:\d\d|\d\d [pa]\.m\.|\d [pa]\.m\.',time) 
    print(time[0] if time != [] else ' ')
    time = time[0] if time != [] else ' '
    dt = parser.parse(date + " " + time);
    data.append(
        {"Title": title,
         "Desc": description,
         "Loc": location,
         'Time': dt.strftime("%Y-%m-%d %H:%M"),
         }
    )
json = json.dumps(data)
files = open("AAData.json", "w")
files.write(json)


