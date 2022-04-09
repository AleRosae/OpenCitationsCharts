import sqlite3
import pandas as pd
import os
import glob
import numpy as np
import zipfile
import gzip
import json
import csv
from alive_progress import alive_bar

connection = sqlite3.connect("crossref_pulito.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS articles (doi TEXT PRIMARY KEY, issn TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS books (doi TEXT PRIMARY KEY, issn TEXT)") #should be isbn not issn
connection.commit()


path = r'E:/opencitation/crossref_2021'
with alive_bar(len(os.listdir(path))) as bar:
    for el in os.listdir(path):
        connection = sqlite3.connect("crossref_pulito.db")
        cursor = connection.cursor()
        to_clean = os.path.join(path, el)
        gzipped = to_clean
        f=gzip.open(gzipped,'rb')
        file_content= json.load(f)
        for record in file_content['items']:
            if 'ISSN' in record.keys():
                doi = record['DOI']
                issn = str(record['ISSN']).strip("']['")
                cursor.execute("INSERT INTO articles VALUES (?, ?)", (doi, issn))
            elif 'ISBN' in record.keys():
                doi = record['DOI']
                isbn = str(record['ISBN']).strip("']['")
                cursor.execute("INSERT INTO books VALUES (?, ?)", (doi, isbn))
            else:
                pass
        connection.commit()
        bar()
cursor.close
connection.close()
        
