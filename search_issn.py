import sqlite3
import csv
import pandas as pd
import glob
import zipfile
import json
import os
import time
import argparse
from alive_progress import alive_bar

parser = argparse.ArgumentParser(description='''Search in the Crossref dump every DOI in COCI in order to get the DOI-ISSN pairs. Requires a list of csv files
                                 as an input (COCI) and either a database or a .csv file containing the Crossref metadata.''')

parser.add_argument("--strategy", required=True, type=str, help='''Method of elaboration. 'db' uses a database file of the crossref dump (slower but less memory impacting);
                                        'csv' uses a .csv file of the dump of crossref (much faster but requires a lot of primary memory). ''')

parser.add_argument("--coci",  required=True, type=str, help="Path to the .csv file of coci that we want to elaborate")
parser.add_argument("--crossref", type=str, required=True, help="Path to the crossref data (either .csv or db) ")
parser.add_argument("--output", required=True, type=str, help="Path for the output results")

args = parser.parse_args()



def get_issn_crossref_withdb(coci_folder, db_path, results_folder, debugging=None): #usando il database del crossref pulito e indicizzato
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  memory_dict = {}
  set_not_found_citing = set()
  set_not_found_cited = set()
  coci_files = [coci_folder+'/'+el for el in os.listdir(coci_folder+'/') if '.csv' in el]
  for coci in coci_files:
    print(coci)
    with open(coci, 'r', encoding="utf8") as csv_file: #read line by line the OC dataset and get citing and cited
      csv_reader = csv.reader(csv_file, delimiter=',')
      row_count = sum(1 for row in csv_reader)  #count the number of rows for the progress bar
      csv_file.seek(0) #reset file and interator
      csv_reader = csv.reader(csv_file, delimiter=',')
      next(csv_reader)
      with alive_bar(row_count,force_tty=True) as bar:
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
  with open(results_folder+'/COCI_processed.json', 'w') as fp:
    json.dump(list(memory_dict.values()), fp) #transform the dict in a list of dicts to reduce the output size 

#counters to check if everything works right
  print('lenght of dict: ', len(memory_dict.keys()))
  print('Number set not found citing: ', len(set_not_found_citing))
  print('Number set not found cited: ', len(set_not_found_cited))

  if debugging != None:
    with open('citing_not_found.csv', 'w') as csvfile: #for debugging
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
  

def get_issn_crossref_witchcsv(coci_files, csv_path, results_folder, debubbing=None): #usando il crossref pulito caricato in memoria
  df_cross = pd.read_csv(csv_path, engine = 'c', 
                         dtype={"doi": 'string', "issn": "string"}) #engine c takes 1m 45s and loads 9GB RAM + 3m 34s and reaches 10.4 GB RAM
  df_cross.set_index('doi', inplace = True)#set the index at the DOI. This FUNDAMENTAL to make the process reasonably fast
  memory_dict = {}
  set_not_found_citing = set()
  set_not_found_cited = set()
  for coci in coci_files:
    with open(coci, 'r', encoding="utf8") as csv_file: #read line by line the OC dataset and get citing and cited
      csv_reader = csv.reader(csv_file, delimiter=',')
      row_count = sum(1 for row in csv_reader)  #count the number of rows for the progress bar
      csv_file.seek(0) #reset file and interator
      csv_reader = csv.reader(csv_file, delimiter=',')
      next(csv_reader)
      with alive_bar(row_count,force_tty=True) as bar:
        for row in csv_reader:
          citing = row[1] #1 if using normal csv instead of 2021
          cited = row[2] #2 if using normal csv instead of 2021
          if citing in memory_dict.keys(): #check if citing has been already searched
            try:
              issn_cited = df_cross.at[cited, 'issn'] #try to get cited issn
              if issn_cited in memory_dict[citing]['has_cited_n_times']:
                memory_dict[citing]['has_cited_n_times'][issn_cited.strip("''")] += 1
              else:
                memory_dict[citing]['has_cited_n_times'][issn_cited.strip("''")] = 1
            except KeyError:
              continue
          elif citing not in set_not_found_citing:
            try:
              issn_citing = df_cross.at[citing, 'issn'] #first search for the citing issn
              if cited not in set_not_found_cited:
                try:
                  issn_cited = df_cross.at[cited, 'issn']#then search for cited issn
                  memory_dict[citing] = {} 
                  memory_dict[citing]['issn'] = issn_citing.strip("''")
                  memory_dict[citing]['has_cited_n_times'] = {}
                  memory_dict[citing]['has_cited_n_times'][issn_cited.strip("''")] = 1
                except KeyError:
                  set_not_found_cited.add(cited)
            except KeyError:
              set_not_found_citing.add(citing)
          bar()
  with open(f'{results_folder}\COCI_processed.json', 'w') as fp:
    json.dump(list(memory_dict.values()), fp) #transform the dict in a list of dicts to reduce the output size 

#counters to check if everything works right
  print('lenght of dict: ', len(memory_dict.keys()))
  print('Number set not found citing: ', len(set_not_found_citing))
  print('Number set not found cited: ', len(set_not_found_cited))

  if debubbing != None:
    with open('citing_not_found.csv', 'w') as csvfile: #for debugging
      writer = csv.writer(csvfile, delimiter=',')
      for line in set_not_found_citing:
        writer.writerow([line])
    csvfile.close()
    with open('cited_not_found.csv', 'w') as csvfile:
      writer = csv.writer(csvfile)
      for line in set_not_found_cited:
        writer.writerow([line])
    csvfile.close()


if __name__ == '__main__':
  if args.strategy == 'csv':
    get_issn_crossref_witchcsv(args.coci, args.crossref, args.output)
  
  elif args.strategy == 'db':
    get_issn_crossref_withdb(args.coci, args.crossref, args.output)
  
  else:
    print('You should provide either a db or a .csv input.')