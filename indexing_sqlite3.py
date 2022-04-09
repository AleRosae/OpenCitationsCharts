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

connection = sqlite3.connect(r"E:/Github desktop/crossref_pulito.db")
cursor = connection.cursor()
index = ("CREATE INDEX doi_index ON articles (doi);")
cursor.execute(index)
connection.commit()
indexed = ("PRAGMA index_list('articles');")
cursor.execute(indexed)
connection.close()