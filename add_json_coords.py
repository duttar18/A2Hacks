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
    gmaps = googlemaps.Client(key='AIzaSyAa7FmyVl9Ip_DJMH6346_i97J_icGb6JI')

    for key in all_jsons.keys():
        data = json.load(all_jsons[key])
        for idx, event in enumerate(data):
            loc = event["Loc"]

            if not loc == " ":
                loc = "{} Ann Arbor, MI".format(loc)
                geocode = gmaps.geocode(loc)
                event['coords'] = geocode[0]['geometry']['location']

            else:
                event['coords'] = " "
        all_jsons[key] = json.dumps(data)

    return all_jsons


if __name__ == '__main__':
    file = 'data.json'

    with open(file, 'r') as f:
        new_json = add_cords({'Monday': f})

        with open("{}-with_coords2.json".format(file[:-5]),'w') as w:
            w.write(new_json["Monday"])
