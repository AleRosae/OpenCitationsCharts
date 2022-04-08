import json

with open(r'D:/GitHub desktop/OpenCitationsCharts/oc-app/src/data/final_results.json', 'r') as fp:
    data = json.load(fp)

print(data.keys())
print(data["areas"].keys())
for k in data["areas"].keys():
    new_areas = []
    for key, value in data['areas'][k].items():
        tmp = {}
        tmp['key'] = key
        tmp['data'] = value
        new_areas.append(tmp)
    data["areas"][k] = new_areas 

print(data['areas'].keys())
print(data['areas']['fields'][:5])

with open(r'C:/Users/alero/Desktop/final_results.json', 'w') as j:
    data = json.dump(data, j)