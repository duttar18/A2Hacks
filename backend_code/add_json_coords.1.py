import json
import googlemaps

def count_cords(file):
    with open(file, 'r') as f:
        data = json.load(f)
        cords = []
        for idx, event in enumerate(data):
            if event["coords"] not in cords:
                cords.append(event["coords"])

        print(len(cords))
        for cord in cords:
            print(cord)

def add_cords(all_jsons):
    gmaps = googlemaps.Client(key='AIzaSyB7eRvuQG86LurkqOGmWuIKykpBf3kRiDI')

    for key in all_jsons.keys():
        data = all_jsons[key]
        for idx, event in enumerate(data):
            loc = event["Loc"]

            if not loc == " ":
                loc = "{} Ann Arbor, MI".format(loc)
                geocode = gmaps.geocode(loc)
                event['coords'] = geocode[0]['geometry']['location']
                print(geocode[0]['geometry']['location'])

            else:
                event['coords'] = " "
        all_jsons[key] = json.dumps(data)

    return all_jsons


if __name__ == '__main__':
    file = 'data_file.json'

    with open(file, 'r') as f:
        new_json = add_cords(json.load(f))
        with open("data_file_with_coords.json",'w') as output:
            json.dump(new_json,output)