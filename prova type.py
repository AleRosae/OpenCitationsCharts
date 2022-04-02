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

path = r'E:/opencitation/crossref'
for el in os.listdir(path):
    to_clean = os.path.join(path, el)
    gzipped = to_clean
    f=gzip.open(gzipped,'rb')
    file_content= json.load(f)
    for record in file_content['items']:
        if record['type'] != 'journal-article':
            print(record['type'], print(record.keys()))
            break

    