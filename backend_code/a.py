import requests, json


with open("data_file_with_coords.json","r") as filesa:
    with open("output.json", "w") as output:
        json.dump(json.JSONDecoder().decode(filesa.read()), output)