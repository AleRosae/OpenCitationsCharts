import json
from numpy.lib.function_base import average
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import parse_COCI
import numpy as np
from zipfile import ZipFile
def initial_parsing(data, asjc_fields = None):
  output_dict = {}
  list_citing= []
  list_cited = []
  n_citations = []
  cited_also_citing = []
  for key, item in data.items():
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

def plot_initial(d, articles = None): #l'informazione dei doi citati è stata persa quindi forse questo grafico non ha molto senso
  if articles == None:
    data = d['tot_citations_distribution']
    ax = sns.histplot(data, log_scale=False, bins= 50)
    fig = ax.get_figure()
  elif articles == 'tot':
    citing = d['citing']
    cited = d['cited']
    fig = plt.figure(figsize=(20,8), dpi= 500)
    plt.pie([citing, cited], labels = ['Only citing', 'Only cited'], autopct='%.0f%%')
  return fig 

def load_data(path):
  with ZipFile(path, 'r') as zip:
    with zip.open('output_2020-04-25T04_48_36_1.json') as infile:
      data = json.load(infile)
      return data



#data = load_data('output_2020-04-25T04_48_36_1.zip')
#result = initial_parsing(data)
#print(result)
#figura = plot_initial(result)
#df_unique_journals = pd.DataFrame({'category': ['citing', 'cited', 'cited_also_citing'], 'value': [result['citing_set'], result['cited_set'], result['cited_also_citing']]})
#print(df_unique_journals)
