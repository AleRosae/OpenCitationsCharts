import json
import pandas as pd
import re
from collections import Counter
from zipfile import ZipFile
import plotly.graph_objects as go
import networkx as nx
from alive_progress import alive_bar
import os

def initial_parsing(data, asjc_fields = None):
  output_dict = {}
  list_citing= []
  list_cited = []
  n_citations = []
  cited_also_citing = []
  for item in data:
    issn = item['issn']
    list_citing.append(issn)
    n_citations.append(sum(item['has_cited_n_times'].values()))
    for k in item['has_cited_n_times']:
      list_cited.append(k)
  citing_set = set(list_citing)
  cited_set = set(list_cited)
  cited_also_citing = citing_set.intersection(cited_set) #cited_also_citing is the intersection between citing and cited
  citing_set = citing_set.difference(cited_set) #citing is the set of citing minus the set of cited
  cited_set = cited_set.difference(citing_set) #cited is only cited that are not in citing
  output_dict["citing"] = len(list_citing)
  output_dict["cited"] = len(list_cited)
  tot = list_citing + list_cited
  tot_journal = set(tot)
  output_dict["journals"] = len(tot_journal)
  output_dict["average_citations"] = round(sum(n_citations) / len(n_citations))
  output_dict["tot_citations_distribution"] = n_citations
  output_dict['cited_also_citing'] = len(cited_also_citing)
  output_dict['citing_set'] = len(citing_set)
  output_dict['cited_set'] = len(cited_set)

  return output_dict

def load_csvs():
  df_issn = pd.read_csv(r'scopus_issn.csv')
  df_issn.drop_duplicates(subset='Print-ISSN', inplace=True)
  df_issn.set_index('Print-ISSN', inplace=True)
  df_asjc = pd.read_csv(r'scopus_asjc.csv')
  df_asjc.set_index('Code', inplace=True)
  df_supergroups = pd.read_csv(r'supergroups.csv')
  df_supergroups.set_index('code', inplace=True)
  output = {'df_issn': df_issn, 'df_asjc':df_asjc, 'df_supergroups': df_supergroups}
  return output

def get_journal_issn(input_issn, csvs, asjc = None, specific_field = None):
  df_issn = csvs['df_issn']
  if asjc: #load the asjc csv and search the disciplinary code in there
    df_asjc = csvs['df_asjc']
    if specific_field != None:
      results = results = {'fields':{}, 'groups':{}, 'supergroups': {}, specific_field.lower():{}}
    else:
      results = {'fields':{}, 'groups':{}, 'supergroups': {}}
      df_supergroups = csvs['df_supergroups']
    for search_issn, value in input_issn.items():
      try:
        tmp = df_issn.at[search_issn, 'ASJC']
        tmp = tmp.split(';')
        field =  df_asjc.at[int(tmp[0].strip()), 'Description'].lower() #only gets the first disciplinary field, which should be the primary one
        if specific_field != None:
          if field.lower() == specific_field.lower():
            results[specific_field.lower()][df_issn.at[search_issn, 'Title']] = int(value)
        else:
          group = df_supergroups.at[str(tmp[0].strip())[:2]+'**', 'Description']
          supergroup = df_supergroups.at[str(tmp[0].strip())[:2]+'**', 'Supergroup']
          if field in results['fields'].keys():
            results['fields'][field] = int(results['fields'][field]) + int(value)
          else:
            results['fields'][field] =  int(value)            
          if group in results['groups'].keys():
            results['groups'][group] = int(results['groups'][group]) + int(value)
          else:
            results['groups'][group] =  int(value)      
          if supergroup in results['supergroups'].keys():
            results['supergroups'][supergroup] = int(results['supergroups'][supergroup]) + int(value)
          else:    
            results['supergroups'][supergroup] = int(value)  
      except KeyError:
        continue
    return results
  else:
    results = []
    for search_issn in input_issn:
      try:
        results.append(df_issn.at[search_issn, 'Title'])
      except KeyError:
        pass #placeholder for ISSN not found
  return results

def parse_data(data, csvs, asjc_fields = False, most_cited = False, 
                specific_field = None):
  output_dict = {}
  counting_all = {}
  if most_cited: #only gets the articles that have been cited
    for item in data:
      for issn in item['has_cited_n_times']:
        counting_all[issn] = counting_all[issn] + item['has_cited_n_times'][issn] 
  else:  
    for item in data:
      issn = item['issn']
      counting_all[issn] = 1
      for issn in item['has_cited_n_times']: #corrispondono a DOI unici nel dataset citazione
        if issn in counting_all.keys():
          counting_all[issn] = counting_all[issn] + item['has_cited_n_times'][issn]
        else:
          counting_all[issn] = item['has_cited_n_times'][issn]
  alt_c = dict(sorted(counting_all.items(), key=lambda item: item[1], reverse=True))
  if asjc_fields: #converts the issn list in disciplinary fields
    if specific_field != None:
      subject = specific_field
      c_asjc = get_journal_issn(alt_c, csvs, asjc=True, specific_field = subject)
      output_dict = c_asjc
    else:
      c_asjc = get_journal_issn(alt_c, csvs, asjc=True)
      output_dict['fields'] = dict(sorted(c_asjc['fields'].items(), key=lambda item: item[1], reverse = True))
      output_dict['groups'] = dict(sorted(c_asjc['groups'].items(), key=lambda item: item[1], reverse = True))
      output_dict['supergroups'] = dict(sorted(c_asjc['supergroups'].items(), key=lambda item: item[1], reverse = True))
  else: 
    new_issn = get_journal_issn(list(alt_c.keys()), csvs)
    values = list(alt_c.values())
    for index, el in enumerate(new_issn):
      output_dict[el] = values[index]
  return output_dict


def self_citation(data, csvs, asjc_fields = None, specific_field = None):
  output_dict = {}
  counter_self = 0
  counter_others = 0
  if specific_field != None and asjc_fields:
      return get_issn_self_citation(data, csvs, specific_field=specific_field)
  elif asjc_fields:
    return get_issn_self_citation(data, csvs)
  else:
    for item in data:
      for k in item['has_cited_n_times'].keys(): 
        if item['issn'] == k:
          counter_self += item['has_cited_n_times'][k]
        else:
          counter_others += item['has_cited_n_times'][k]
    output_dict['self'] = counter_self
    output_dict['not self'] = counter_others
  return output_dict
    
def get_issn_self_citation(data, csvs, specific_field = None): #particolarmente pesante se fatta per i field perché deve convertirli tutti
  self_citations = 0
  partial_self_citations = 0
  not_self_citations = 0
  not_found = 0 #il numero di citazioni per cui l'issn associato non si riesce a trovare nel csv 
  df_issn = csvs['df_issn']
  df_asjc = csvs['df_asjc']
  if specific_field != None:
    for row in df_asjc.itertuples():
      if row[1].lower() == specific_field.lower():
        specific_code = str(row[0])
  results = {}
  for value in data:
    try:
      search_issn = value['issn']
      citing_code = df_issn.at[search_issn, 'ASJC']
      citing_code = citing_code.split(';')[0]
      if specific_field == None:
        for search_cited in value['has_cited_n_times'].keys():  
          try:
            cited_code = df_issn.at[search_cited, 'ASJC']
            cited_code = cited_code.split(';')[0]
            if citing_code == cited_code:
              self_citations += value['has_cited_n_times'][search_cited]
            elif citing_code[:1] == cited_code[:1]:
              partial_self_citations += value['has_cited_n_times'][search_cited]
            else:
              not_self_citations += value['has_cited_n_times'][search_cited]
          except KeyError:
            not_found += value['has_cited_n_times'][search_cited]
      else:        
        for search_cited in value['has_cited_n_times'].keys():  
          try:          
            cited_code = df_issn.at[search_cited, 'ASJC']
            cited_code = cited_code.split(';')[0]
            if citing_code == cited_code and citing_code == specific_code:
              self_citations += value['has_cited_n_times'][search_cited]
            elif citing_code[:1] == cited_code[:1] and citing_code == specific_code:
              partial_self_citations += value['has_cited_n_times'][search_cited]
            elif citing_code == specific_code:
              not_self_citations += value['has_cited_n_times'][search_cited]
          except KeyError:
              not_found += value['has_cited_n_times'][search_cited]
    except KeyError:
      continue        
  results['self'] = self_citations
  results['partial self'] = partial_self_citations
  results['not self']  = not_self_citations
  #results['not_found'] = not_found
  return results

def load_data(folder, zip=None):
  path = os.path.join(folder, 'COCI_processed.json')
  if zip == False:
    with open(path, 'r') as fp:
      data = json.load(fp)
      return data
  else:
    with ZipFile(path, 'r') as zip:
      f_json = path.replace('.zip', '.json')
      with zip.open(f_json) as infile:
        data = json.load(infile)
        return data

def spelling_mistakes(input_data, journal = None):
    result = {}
    if not journal:
      df_asjc = pd.read_csv(r'scopus_asjc.csv')
      ajsc = df_asjc['Description'].tolist()
      asjc = [x.lower() for x in ajsc]
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
    else:
      df_issn = pd.read_csv(r'scopus_issn.csv')
      issn = df_issn['Title'].to_list()
      issn = [title.lower() for title in issn]
      if input_data.lower() in issn:
        result[input_data] = False
      else:
        for el in issn:
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


def citations_flow(data, csvs, specific_field = None):
  output_dict = {'fields':{}, 'groups':{}, 'supergroups': {}}
  df_issn = csvs['df_issn']
  df_asjc = csvs['df_asjc']
  df_supergroups = csvs['df_supergroups']
  for item in data:
    search_issn = item['issn']
    try:
      tmp = df_issn.at[search_issn, 'ASJC']
    except KeyError:
      continue
    tmp = tmp.split(';')
    field_citing =  df_asjc.at[int(tmp[0].strip()), 'Description']
    if field_citing.lower() == specific_field.lower():
      for issn_cited in item['has_cited_n_times']: #corrispondono a DOI unici nel dataset citazione
        try:
          tmp_cited= df_issn.at[issn_cited, 'ASJC']
        except KeyError:
          continue
        tmp_cited = tmp_cited.split(';')
        field_cited =  df_asjc.at[int(tmp_cited[0].strip()), 'Description']
        group = df_supergroups.at[str(tmp_cited[0].strip())[:2]+'**', 'Description']
        supergroup = df_supergroups.at[str(tmp_cited[0].strip())[:2]+'**', 'Supergroup']
        if field_cited.lower() != specific_field.lower(): 
          if field_cited in output_dict['fields'].keys():
            output_dict['fields'][field_cited] += item['has_cited_n_times'][issn_cited]
          else:
            output_dict['fields'][field_cited] = item['has_cited_n_times'][issn_cited]           
          if group in output_dict['groups'].keys():
            output_dict['groups'][group] += item['has_cited_n_times'][issn_cited]
          else:
            output_dict['groups'][group] = item['has_cited_n_times'][issn_cited]      
          if supergroup in output_dict['supergroups'].keys():
            output_dict['supergroups'][supergroup] += item['has_cited_n_times'][issn_cited]
          else:    
            output_dict['supergroups'][supergroup] =  item['has_cited_n_times'][issn_cited] 
        else:
          continue
    else:
      continue
  output_dict['fields'] = dict(sorted(output_dict['fields'].items(), key=lambda item: item[1], reverse = True))
  output_dict['groups'] = dict(sorted(output_dict['groups'].items(), key=lambda item: item[1], reverse = True))
  output_dict['supergroups'] = dict(sorted(output_dict['supergroups'].items(), key=lambda item: item[1], reverse = True))
  return output_dict
  
def citations_flow_journals(data, csvs):
  output_dict = {}
  df_issn = csvs['df_issn']
  df_asjc = csvs['df_asjc']
  fields_tmp = df_asjc['Description'].tolist()
  tot_comb = []
  for el in fields_tmp:
      for f in fields_tmp:
          tot_comb.append((el.lower(), f.lower())) 
  with alive_bar(len(data)) as bar:
    for item in data:
      search_issn = item['issn']
      try:
        journal_citing = df_issn.at[search_issn, 'Title']
        tmp = df_issn.at[search_issn, 'ASJC']
      except KeyError:
        continue
      tmp = tmp.split(';')
      field_citing =  df_asjc.at[int(tmp[0].strip()), 'Description']
      citing_comb = [el for el in tot_comb if field_citing.lower() == el[0]]

      for issn_cited in item['has_cited_n_times']: 
        try:
          tmp_cited= df_issn.at[issn_cited, 'ASJC']
          journal_cited = df_issn.at[issn_cited, 'Title']
        except KeyError:
          continue
        tmp_cited = tmp_cited.split(';')
        field_cited =  df_asjc.at[int(tmp_cited[0].strip()), 'Description']
        cited_comb = [el for el in citing_comb if field_cited.lower() == el[1]]
        comb = str(cited_comb[0])
        if comb not in output_dict.keys():
          output_dict[comb] = {}
          output_dict[comb][journal_cited] = item['has_cited_n_times'][issn_cited]
        else:
          if journal_cited in output_dict[comb].keys():
            output_dict[comb][journal_cited] += item['has_cited_n_times'][issn_cited]
          else:
            output_dict[comb][journal_cited] = item['has_cited_n_times'][issn_cited]
      bar()

  #output_dict = dict(sorted(output_dict.items(), key=lambda item: item[1], reverse = True))
  return output_dict

#data = load_data('prova_result_db.zip')
#comb = citations_flow_journals(data, csvs=load_csvs())
#print(comb)

def check_unmentioned(data):
  df_supergroups = pd.read_csv(r'supergroups.csv')
  df_supergroups.set_index('code', inplace=True)
  result = []
  list_fields = df_supergroups['Description'].to_list()
  for el in list_fields:
    if el not in data.keys():
      result.append(el)
  return result
      

def search_specific_journal(data, csvs):
  output_dict = {}
  df_issn = csvs['df_issn']
  df_asjc = csvs['df_asjc']
  df_supergroups = csvs['df_supergroups']
  with alive_bar(len(data)) as bar:
    for item in data:
      bar()
      search_issn = item['issn']
      try:
        journal = df_issn.at[search_issn, 'Title']
      except KeyError:
        continue
      code = df_issn.at[search_issn, 'ASJC']
      code = code.split(';')[0]
      field = df_asjc.at[int(code), 'Description']
      group = df_supergroups.at[code[:2].strip()+'**', 'Description']
      title = journal.lower()
      if title not in output_dict.keys():
        output_dict[title] = {}
        output_dict[title]['field'] = field
        output_dict[title]['group'] = group
        output_dict[title]['citations'] = {}
      for k in item['has_cited_n_times']: 
        cited_issn = re.sub("-", "", k)
        cited_issn = re.sub("'", "", cited_issn)
        try:
          title_cited = df_issn.at[cited_issn, 'Title']
        except KeyError:
          continue
        if title_cited in output_dict[title]['citations'].keys():
          output_dict[title]['citations'][title_cited] += item['has_cited_n_times'][k]
        else:
          output_dict[title]['citations'][title_cited] = item['has_cited_n_times'][k]

      output_dict[title]['citations'] = dict(sorted(output_dict[title]['citations'].items(), key=lambda item: item[1], reverse = True))

  return output_dict


def citations_networks(data):
  output_dict = {}
  df_issn = pd.read_csv(r'scopus_issn.csv')
  df_issn.drop_duplicates(subset='Print-ISSN', inplace=True)
  df_issn.set_index('Print-ISSN', inplace=True)
  df_asjc = pd.read_csv(r'scopus_asjc.csv')
  df_asjc.set_index('Code', inplace=True)
  df_supergroups = pd.read_csv(r'supergroups.csv')
  df_supergroups.set_index('code', inplace=True)
  for item in data:
    search_issn = item['issn']
    try:
      tmp_citing = df_issn.at[search_issn, 'ASJC']
    except KeyError:
      continue
    tmp_citing = tmp_citing.split(';')
    group_citing = df_supergroups.at[str(tmp_citing[0].strip())[:2]+'**', 'Description']
    for k in item['has_cited_n_times']: #corrispondono a DOI unici nel dataset citazione
      issn_cited = re.sub('-', "", k)
      issn_cited = re.sub("'", "", issn_cited)
      try:
        tmp_cited= df_issn.at[issn_cited, 'ASJC']
      except KeyError:
        continue
      tmp_cited = tmp_cited.split(';')
      group_cited = df_supergroups.at[str(tmp_cited[0].strip())[:2]+'**', 'Description']
      if group_citing in output_dict.keys() and group_cited in output_dict[group_citing].keys():
        output_dict[group_citing][group_cited] += item['has_cited_n_times'][k]
      elif group_citing in output_dict.keys():
        output_dict[group_citing][group_cited] = item['has_cited_n_times'][k]
      else:
        output_dict[group_citing] = {}
        output_dict[group_citing][group_cited] = item['has_cited_n_times'][k]
  return output_dict


def query_self_citation(data, csvs):
  df_issn = csvs['df_issn']
  df_asjc = csvs['df_asjc']
  results = {}
  with alive_bar(len(data)) as bar:
    for value in data:
      self_citations = 0
      partial_self_citations = 0
      not_self_citations = 0
      bar()
      try:
        search_issn = value['issn']
        citing_code = df_issn.at[search_issn, 'ASJC']
        citing_code = citing_code.split(';')[0]
        citing_field =  df_asjc.at[int(citing_code.strip()), 'Description'].lower()         
        for search_cited in value['has_cited_n_times'].keys():  
          try:         
            cited_code = df_issn.at[search_cited, 'ASJC']
            cited_code = cited_code.split(';')[0]
            if citing_code == cited_code:
              self_citations += value['has_cited_n_times'][search_cited]
            elif citing_code[:1] == cited_code[:1]:
              partial_self_citations += value['has_cited_n_times'][search_cited]
            else:
              not_self_citations += value['has_cited_n_times'][search_cited]
          except KeyError:
              continue
        if citing_field not in results.keys():
          results[citing_field] = {}
          results[citing_field]['self'] = self_citations
          results[citing_field]['partial self'] = partial_self_citations
          results[citing_field]['not self']  = not_self_citations
        else:
          results[citing_field]['self'] += self_citations
          results[citing_field]['partial self'] += partial_self_citations
          results[citing_field]['not self'] += not_self_citations
      except KeyError:
        continue     
       
      

  return results



def make_edge(x, y, text, width):
    return  go.Scatter(x         = x,
                      y         = y,
                      line      = dict(width = width,
                                  color = 'cornflowerblue'),
                      
                      hoverinfo = 'text',
                      text      = ([text]),
                      mode      = 'lines')
    
def creat_vis_graph(d, tot):
  graph = nx.Graph()
  for key, value in d.items():
    graph.add_node(key, size=sum(value.values())/tot)
    for k, v in value.items():
      graph.add_edge(key, k, weight=v / tot)
  pos = nx.spring_layout(graph)
  # For each edge, make an edge_trace, append to list
  edge_trace = []
  for edge in graph.edges():
          field_1 = edge[0]
          field_2 = edge[1]
          x0, y0 = pos[field_1]
          x1, y1 = pos[field_2]
          text = field_1 + '--' + field_2 + ': ' + str(graph.edges()[edge]['weight'] )
          trace  = make_edge([x0, x1, None], [y0, y1, None], text, 
                            width = graph.edges()[edge]['weight'])
          edge_trace.append(trace)
  node_trace = go.Scatter(x         = [],
                          y         = [],
                          text      = [],
                          textposition = "top center",
                          textfont_size = 10,
                          mode      = 'markers+text',
                          hoverinfo = 'text',
                          marker    = dict(colorscale='Viridis',
                                              reversescale=False,
                                              color=[],
                                              size = [],
                                            ))
  for node in graph.nodes():
      x, y = pos[node]
      node_trace['x'] += tuple([x])
      node_trace['y'] += tuple([y])
      node_trace['marker']['color'] += tuple(['cornflowerblue'])
      node_trace['marker']['size'] += tuple([graph.nodes()[node]['size']])
      node_trace['text'] += tuple(['<b>' + node + '</b>'])
  # Customize layout
  layout = go.Layout(
      height = 800,
      paper_bgcolor='rgba(0,0,0,0)', # transparent background
      plot_bgcolor='rgba(0,0,0,0)', # transparent 2nd background
      xaxis =  {'showgrid': False, 'zeroline': False}, # no gridlines
      yaxis = {'showgrid': False, 'zeroline': False}, # no gridlines.
        hovermode='closest',
    margin=dict(b=20,l=5,r=5,t=40),
  )
  node_adjacencies = []
  node_text = []
  for node, adjacencies in enumerate(graph.adjacency()):
      node_adjacencies.append(len(adjacencies[1]))
      node_text.append('# of connections: '+str(len(adjacencies[1])))

  node_trace.marker.color = node_adjacencies
  # Create figure
  fig = go.Figure(layout = layout)
  # Add all edge traces
  for trace in edge_trace:
      fig.add_trace(trace)
  # Add node trace
  fig.add_trace(node_trace)
  # Remove legend
  fig.update_layout(showlegend = False, 
        title={
        'text': '<b>Citations network</b>',
        'x': 0.5,
        'xanchor': 'center'
      })
  # Remove tick labels
  fig.update_xaxes(showticklabels = False)
  fig.update_yaxes(showticklabels = False)
  # Show figure
  return fig


def create_gephi_data(folder):
  with open (folder + r'/final_results.json', 'r') as f:
    data = json.load(f)
  edges = {'target': [], 'source': [], 'weight': []}
  nodes = {'id': [], 'label': []}

  for key, value in data['net'].items():
    for el, weight in value.items():
      edges['target'].append(key)
      edges['source'].append(el)
      edges['weight'].append(weight/sum(value.values()))
  nodes['id'] = list(data['net'].keys())
  nodes['label'] = list(data['net'].keys())
  
  df = pd.DataFrame.from_dict(edges)
  df.to_csv('edges.csv', index = False)
  df = pd.DataFrame.from_dict(nodes)
  df.to_csv('nodes.csv', index = None)


