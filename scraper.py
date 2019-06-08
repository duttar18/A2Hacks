from lxml import html
import requests

page = requests.get("https://events.umich.edu/day");
tree = html.fromstring(page.content);

titles = tree.xpath('//div[@class="event-info"]/p/text()');
locations = tree.xpath('//ul[@class="event-details"]/li[1]/a/@title');
times = tree.xpath('//div[@class="event-listing             "]/time/@datetime');
print(times);
