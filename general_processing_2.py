import json

with open(r'D:/GitHub desktop/OpenCitationsCharts/oc-app/src/data/final_results.json', 'r') as fp:
    data = json.load(fp)

#print(data.keys())
#print(data["init"].keys())
new_selfcit= []
for key, value in data['self_cit_area'].items():
    tmp = {}
    tmp['key'] = key
    tmp['data'] = value
    new_selfcit.append(tmp)

data['self_cit_area'] = new_selfcit  

print(data['self_cit_area'])
with open(r'C:/Users/alero/Desktop/final_results.json', 'w') as j:
    data = json.dump(data, j)