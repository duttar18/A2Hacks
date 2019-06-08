from lxml import html
import requests, json

page = requests.get("https://events.umich.edu/day")
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
    print(location)
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
json = json.dumps(data);
files = open("MData.json", "w");
files.write(json);


