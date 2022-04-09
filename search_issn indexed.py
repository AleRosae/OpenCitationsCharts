import sqlite3
import csv
import pandas as pd
import glob
import zipfile
import json
import os
import time
from alive_progress import alive_bar


def get_issn_crossref(coci_files):
  db_path = 'E:/Github desktop/crossref_pulito_indexed.db'
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  memory_dict = {}
  set_not_found_citing = set()
  set_not_found_cited = set()
  for coci in coci_files:
    print(coci)
    with open(coci, 'r', encoding="utf8") as csv_file: #read line by line the OC dataset and get citing and cited
      csv_reader = csv.reader(csv_file, delimiter=',')
      row_count = sum(1 for row in csv_reader)  #count the number of rows for the progress bar
      csv_file.seek(0) #reset file and interator
      csv_reader = csv.reader(csv_file, delimiter=',')
      next(csv_reader)
      with alive_bar(row_count) as bar:
        for row in csv_reader:
          citing = row[1] 
          cited = row[2] 
          if citing in memory_dict.keys(): #check if citing has been already searched
            rows = cursor.execute(
                  "SELECT doi, issn FROM articles WHERE doi = ?",
                          (cited,),).fetchall()  
            if len(rows) != 0:
              issn_cited = rows[0][1]
              issn_cited = issn_cited.split(', ')[0].strip("'").replace("-", "") #we are getting only the e-issn instead of the printed one
              if issn_cited in memory_dict[citing]['has_cited_n_times']:
                memory_dict[citing]['has_cited_n_times'][issn_cited.strip("''")] += 1
              else:
                memory_dict[citing]['has_cited_n_times'][issn_cited.strip("''")] = 1
            else:
              continue
          elif citing not in set_not_found_citing:
            rows = cursor.execute(
                  "SELECT doi, issn FROM articles WHERE doi = ?",
                          (citing,),).fetchall() 
            if len(rows) != 0: 
              issn_citing = rows[0][1]
              issn_citing = issn_citing.split(', ')[0].strip("'").replace("-", "")
              if cited not in set_not_found_cited:
                rows = cursor.execute(
                  "SELECT doi, issn FROM articles WHERE doi = ?",
                          (cited,),).fetchall()  
                if len(rows) != 0:
                  issn_cited = rows[0][1]
                  issn_cited = issn_cited.split(', ')[0].strip("'").replace("-", "")
                  memory_dict[citing] = {} 
                  memory_dict[citing]['issn'] = issn_citing.strip("''")
                  memory_dict[citing]['has_cited_n_times'] = {}
                  memory_dict[citing]['has_cited_n_times'][issn_cited.strip("''")] = 1
                else:
                  set_not_found_cited.add(cited)
            else:
              set_not_found_citing.add(citing)
          bar()
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

  connection.close()

get_issn_crossref([r'E:/opencitation/6741422/2020-08-20T18_12_28_1-2/'+el for el in os.listdir('E:/opencitation/6741422/2020-08-20T18_12_28_1-2/') if '.csv' in el])