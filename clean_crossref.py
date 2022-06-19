"""

This notebook is meant to severely reduce the size of the Crossref dataset (which is about 60 GB zipped) in order to speed up the computation. This is mainly done by keeping only the relevant information for the project, i.e. the DOI of the article and the ISSN of its journal. 
The notebook has been run on a local runtime to access files stored locally.
"""
import os
import pandas as pd
import numpy as np
import gzip
import json
import argparse
from alive_progress import alive_bar


parser = argparse.ArgumentParser(description='Clean the crossref dump (already unzipped) and gives as output a .csv with only DOI and ISSN as colums')


parser.add_argument("--input",  required=True, type=str, help="String. Path of crossref dump unzipped")
parser.add_argument("--split", type=int, help="Integer. Split every x DOI processed in order to get smaller .csv file that can be merged afterwards")
parser.add_argument("--output", required=True, type=str, help="String. Path for the output results")

args = parser.parse_args()


def clean_crossref(path_input, path_output, split = None):
  #path = r'E:/opencitation/crossref' #path di crossref unzippato
  dois = []
  issns = []
  counter = 0
  with alive_bar(len(os.listdir(path_input))) as bar:
    for el in os.listdir(path_input):
      bar()
      to_clean = os.path.join(path_input, el)
      gzipped = to_clean
      f=gzip.open(gzipped,'rb')
      file_content= json.load(f)
      for record in file_content['items']:
        if 'ISSN' in record.keys():
          dois.append(record['DOI'])
          issns.append(str(record['ISSN']).strip("']['")) #issns.append(str(record['ISSN'][0]).strip("']['")) se vogliamo prendere solo un ISSN
        else:
          pass
      #questo blocco si attiva dopo ogni elemento del for loop principale
      if split != None: #splitta se non si ha abbastanza ram a disposizione
        if len(dois) > split:
          counter += 1
          df = pd.DataFrame(data = list(zip(dois, issns)), columns=['doi', 'issn'])
          df.to_csv(path_output + r'/prova_'+str(counter) + '.csv', index= False)
          dois = []
          issns = []
          #print(f'number of csv: {str(counter)}')
  counter += 1
  df = pd.DataFrame(data = list(zip(dois, issns)), columns=['doi', 'issn']) #crea df finale
  df.to_csv(path_output + r'/prova_'+str(counter) + '.csv', index= False)

if __name__ == "__main__":
    clean_crossref(args.input, args.output, args.split)
    print('done!')
