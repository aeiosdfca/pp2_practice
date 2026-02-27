# json syntax

{
  "employees": [
    {"firstimya": "Venera", "lastfamiliya": "Sadyrova"},
    {"firstimya": "Jane", "lastfamiliya": "Doe"},
    {"firstimya": "Kirill", "lastfamiliya": "Flins"}
  ]
}


# parsing JSON with json.loads()

import json  
json_str = '{"name": "Igor", "age": 18, "city": "Seoul"}'
data = json.loads(json_str)  
print(data["city"])


# writing, converting python to JSON with (json.dumps()) and reading them

person = '{"name": "Igor", "age": 18, "city": "Seoul"}'
json_data = json.dumps(person, indent=2)
print(json_data)

with open("person.json", "w") as f:
    json.dump(person, f)

with open("sample-data.json", "r") as f:
    data = json.load(f)     
print(data)


# working with data in JSON

data = {"employees": [{"firstName": "Venera", "lastName": "Sadyrova"},
                      {"firstName": "Jane", "lastName": "Doe"}]}
names = [emp["firstName"] for emp in data["employees"]]
print(names) 