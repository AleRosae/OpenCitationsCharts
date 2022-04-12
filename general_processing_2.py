import json
import pandas as pd

with open(r'D:/GitHub desktop/OpenCitationsCharts/oc-web/final_results.json', 'r') as fp:
    data = json.load(fp)

new_net = []
for key, value in data['net'].items():
    for k, v in value.items():
        tmp = {'from':key, 'to': k, 'value': v}
        new_net.append(tmp)
print(new_net[:5])    
data['net'] = new_net

with open(r'C:/Users/alero/Desktop/final_results.json', 'w') as j:
   data = json.dump(data, j)