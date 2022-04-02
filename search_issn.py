import sqlite3
import csv
import pandas as pd
import glob
import zipfile
import json
import os
import time

connection = sqlite3.connect("crossref_pulito.db")
cursor = connection.cursor()
rows = cursor.execute(
                "SELECT Count() from articles").fetchall()  
print(rows)

connection.close()

def get_issn_crossref(coci_files):
  memory_dict = {}
  set_not_found_citing = set()
  set_not_found_cited = set()
  for coci in coci_files:
    print(coci)
    with open(coci, 'r') as csv_file: #read line by line the OC dataset and get citing and cited
      csv_reader = csv.reader(csv_file, delimiter=',')
      next(csv_reader)
      for row in csv_reader:
        citing = row[1] #1 if using normal csv instead of 2021
        cited = row[2] #2 if using normal csv instead of 2021
        if citing in memory_dict.keys(): #check if citing has been already searched
          try:
            rows = cursor.execute(
                "SELECT doi, issn FROM articles WHERE doi = ?",
                        (cited,),).fetchall()  
            issn_cited = rows[0][1]
            if issn_cited in memory_dict[citing]['has_cited_n_times']:
              memory_dict[citing]['has_cited_n_times'][issn_cited.strip("''")] += 1
            else:
              memory_dict[citing]['has_cited_n_times'][issn_cited.strip("''")] = 1
          except KeyError:
            continue
        elif citing not in set_not_found_citing:
          try:
            rows = cursor.execute(
                "SELECT doi, issn FROM articles WHERE doi = ?",
                        (citing,),).fetchall()  
            issn_citing = rows[0][1]
            if cited not in set_not_found_cited:
              try:
                rows = cursor.execute(
                "SELECT doi, issn FROM articles WHERE doi = ?",
                        (cited,),).fetchall()  
                issn_cited = rows[0][1]
                memory_dict[citing] = {} 
                memory_dict[citing]['issn'] = issn_citing.strip("''")
                memory_dict[citing]['has_cited_n_times'] = {}
                memory_dict[citing]['has_cited_n_times'][issn_cited.strip("''")] = 1
              except KeyError:
                set_not_found_cited.add(cited)
          except KeyError:
            set_not_found_citing.add(citing)
  with open('prova.json', 'w') as fp:
    json.dump(list(memory_dict.values()), fp) #transform the dict in a list of dicts to reduce the output size 

#counters to check if everything works right
  print('lenght of dict: ', len(memory_dict.keys()))
  print('Number set not found citing: ', len(set_not_found_citing))
  print('Number set not found cited: ', len(set_not_found_cited))

  with open('citing_not_found.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for line in set_not_found_citing:
      writer.writerow([line])
  csvfile.close()
  with open('cited_not_found.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for line in set_not_found_cited:
      writer.writerow([line])
  csvfile.close()

#get_issn_crossref([r'E:/opencitation/6741422/2020-08-20T18_12_28_1-2/'+el for el in os.listdir('E:/opencitation/6741422/2020-08-20T18_12_28_1-2/') if '.csv' in el])