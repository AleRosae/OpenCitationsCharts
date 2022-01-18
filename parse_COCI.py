import json
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
from streamlit.state.session_state import Value
from zipfile import ZipFile

def get_journal_issn(input_issn, asjc = None, specific_field = None):
  df_issn = pd.read_csv(r'scopus_issn.csv')
  df_issn.drop_duplicates(subset='Print-ISSN', inplace=True)
  df_issn.set_index('Print-ISSN', inplace=True)
  if asjc: #load the asjc csv and search the disciplinary code in there
    results = {}
    df_asjc = pd.read_csv(r'scopus_asjc.csv')
    df_asjc.set_index('Code', inplace=True)
    for issn, value in input_issn.items():
      try:
        search_issn = re.sub("'", "", issn)
        tmp = df_issn.at[search_issn, 'ASJC']
        tmp = tmp.split(';')
        field =  df_asjc.at[int(tmp[0].strip()), 'Description'] #only gets the first disciplinary field, which should be the primary one
        if specific_field != None:
          if field.lower() == specific_field.lower():
            results[df_issn.at[search_issn, 'Title']] = int(value)
        else:
          if field in results.keys():
            results[field] = int(results[field]) + int(value)
          else:
            results[field] =  int(value)
      except KeyError:
        continue
    return results
  else:
    results = []
    for issn in input_issn:
      search_issn = re.sub("'", "", issn)
      try:
        results.append(df_issn.at[search_issn, 'Title'])
      except KeyError:
        pass #placeholder for ISSN not found
  return results

def parse_data(data, n = None, asjc_fields = False, most_cited = False, 
                specific_field = None):
  if n == None:
    n = 10
  output_dict = {}
  counting_all = {}
  if most_cited: #only gets the articles that have been cited
    for item in data:
      for k in item['has_cited_n_times']:
        issn = re.sub('-', "", k)
        counting_all[issn] = counting_all[issn] + item['has_cited_n_times'][k] 
  else:  
    for item in data:
      issn = item['issn']
      issn = re.sub('-', "", issn)
      counting_all[issn] = 1
      for k in item['has_cited_n_times']: #corrispondono a DOI unici nel dataset citazione
        issn = re.sub('-', "", k)
        if issn in counting_all.keys():
          counting_all[issn] = counting_all[issn] + item['has_cited_n_times'][k]
        else:
          counting_all[issn] = item['has_cited_n_times'][k]
  alt_c = dict(sorted(counting_all.items(), key=lambda item: item[1], reverse=True))
  if asjc_fields: #converts the issn list in disciplinary fields
    if specific_field != None:
      subject = specific_field
      c_asjc = get_journal_issn(alt_c, asjc=True, specific_field = subject)
      output_dict = c_asjc
    else:
      c_asjc = get_journal_issn(alt_c, asjc=True)
      c_asjc = dict(sorted(c_asjc.items(), key=lambda item: item[1], reverse = True))
      counter = 0
      for key, value in c_asjc.items():
        output_dict[key] = value
        counter +=1
        if n != 'all' and counter == n:
          break
  else: 
    new_issn = get_journal_issn(list(alt_c.keys()))
    values = list(alt_c.values())
    counter = 0
    for index, el in enumerate(new_issn):
      output_dict[el] = values[index]
      counter += 1
      if n != 'all' and counter == n:
        break
  return output_dict

 #deprecated
def plot_statistics(data, most_cited = None, asjc_fields = None, specific_field = None, comparison = None):
  if most_cited and asjc_fields:
    x_label= 'Fields'
    output = parse_data(data, asjc_fields=True, most_cited=True)
  elif asjc_fields and specific_field:
    counter = 0
    x_label = 'Journals'
    output = {}
    for key, value in data.items():
      output[key] = value
      counter += 1
      if counter > 10:
        break    
  elif most_cited:
    output = parse_data(data, most_cited=True)
    x_label = 'Journals'
  elif asjc_fields:
    output = parse_data(data, asjc_fields=True)
    x_label = 'Fields'
  elif comparison:
    output = data
    x_label = 'Fields'
  else:
    output = parse_data(data)
    x_label = 'Journals'
  label_list = []
  x = list(output.keys())
  y = output.values()
  for index, el in enumerate(x):
    if x_label == 'Fields':
      max = 45
    else:
      max = 25
    if len(el) > max:
      tmp_str = [char for char in el if char.isupper()]
      new = "".join(tmp_str)
      x[index] = new
      label_list.append(new+' = '+el)
  legend = "\n".join(label_list)
  fig = plt.figure(figsize=(20,8), dpi= 500)
  plt.xlabel(x_label)
  plt.ylabel('amount')
  #plt.title('top 10 journals in OC dataset')
  plt.text(0.70, 0.85, legend, 
          fontsize=10, color='k',
          ha='left', va='bottom',
          transform=plt.gca().transAxes)
  plt.style.use('seaborn-pastel')
  #plt.xticks(rotation=90)
  plt.bar(x,y)
  for index,data in enumerate(y):
      plt.text(x=index , y =data+1 , s=f"{data}" , fontdict=dict(fontsize=12), horizontalalignment="center", verticalalignment="top")

  return fig

def self_citation(data, asjc_fields = None, specific_field = None):
  output_dict = {}
  counter_self = 0
  counter_others = 0
  if specific_field != None and asjc_fields:
      return get_issn_self_citation(data, specific_field=specific_field)
  elif asjc_fields:
    return get_issn_self_citation(data)
  else:
    for item in data:
      for k in item['has_cited_n_times'].keys(): 
        if item['issn'] == k:
          counter_self += item['has_cited_n_times'][k]
        else:
          counter_others += item['has_cited_n_times'][k]
    tot = counter_self + counter_others
    output_dict['self ('+str(round((counter_self/tot) * 100))+'%)'] = counter_self
    output_dict['not self ('+str(round((counter_others/tot) * 100))+'%)'] = counter_others
  return output_dict
    
def get_issn_self_citation(data, specific_field = None): #particolarmente pesante se fatta per i field perché deve convertirli tutti
  self_citations = 0
  partial_self_citations = 0
  not_self_citations = 0
  not_found = 0 #il numero di citazioni per cui l'issn associato non si riesce a trovare nel csv 
  df_issn = pd.read_csv(r'scopus_issn.csv')
  df_issn.drop_duplicates(subset='Print-ISSN', inplace=True)
  df_issn.set_index('Print-ISSN', inplace=True)
  df_asjc = pd.read_csv(r'scopus_asjc.csv') #carica entrambi i csv perché servono per cercare field specifico
  df_asjc.set_index('Code', inplace=True)  
  results = {}
  for value in data:
    try:
      search_issn = re.sub("'", "", value['issn'])
      search_issn = re.sub("-", "", search_issn)
      citing_code = df_issn.at[search_issn, 'ASJC']
      citing_code = citing_code.split(';')[0]
      if specific_field == None:
        for k in value['has_cited_n_times'].keys():  
          try:
            search_cited= re.sub("'", "", k)
            search_cited = re.sub("-", "", search_cited)
            cited_code = df_issn.at[search_cited, 'ASJC']
            cited_code = cited_code.split(';')[0]
            if citing_code == cited_code:
              self_citations += value['has_cited_n_times'][k]
            elif citing_code[:1] == cited_code[:1]:
              partial_self_citations += value['has_cited_n_times'][k]
            else:
              not_self_citations += value['has_cited_n_times'][k]
          except KeyError:
            not_found += value['has_cited_n_times'][k]
      else:        
        for k in value['has_cited_n_times'].keys():  
          try:          
            search_cited= re.sub("'", "", k)
            search_cited = re.sub("-", "", search_cited)
            cited_code = df_issn.at[search_cited, 'ASJC']
            cited_code = cited_code.split(';')[0]
            field =  df_asjc.at[int(citing_code.strip()), 'Description'] #only gets the first disciplinary field, which should be the primary one
            if field.lower() == specific_field.lower():#prendi solo quelli che hanno field uguale a quello di input
              if citing_code == cited_code:
                self_citations += value['has_cited_n_times'][k]
              elif citing_code[:1] == cited_code[:1]:
                partial_self_citations += value['has_cited_n_times'][k]
              else:
                not_self_citations += value['has_cited_n_times'][k]
            else:
              continue  
          except KeyError:
              not_found += value['has_cited_n_times'][k]
    except KeyError:
      continue        
  tot = self_citations + partial_self_citations + not_self_citations
  results['self ('+str(round((self_citations/tot) * 100))+'%)'] = self_citations
  results['partial self ('+str(round((partial_self_citations/tot) * 100))+'%)'] = partial_self_citations
  results['not self ('+str(round((not_self_citations/tot) * 100))+'%)']  = not_self_citations
  #results['not_found'] = not_found
  return results

def load_data(path):
  with ZipFile(path, 'r') as zip:
    with zip.open('output_2020-04-25T04_48_36_1.json') as infile:
      data = json.load(infile)
      return data

def spelling_mistakes(input_data):
    df_asjc = pd.read_csv(r'scopus_asjc.csv')
    ajsc = df_asjc['Description'].tolist()
    asjc = [x.lower() for x in ajsc]
    result = {}
    if input_data.lower() in asjc:
      result[input_data] = False
    else:
      for el in asjc:
        if input_data.lower() in el.lower() and input_data not in result.keys():
          result[input_data] = []
          result[input_data].append(el)
        elif input_data.lower() in el.lower() and input_data in result.keys():
          result[input_data].append(el)
    if len(result.keys()) == 0:
      result = None
    elif not any(result.values()) and not type(list(result.values())[0]) == str:
      result = False
    return result


#data = load_data('output_2020-04-25T04_48_36_1.zip')
#print(parse_data(data, asjc_fields=True))
#print(self_citation(data, asjc_fields=True, specific_field='Philosophy'))
#print(spelling_mistakes('medicine'))