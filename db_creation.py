import sqlite3
import os
import gzip
import json
import argparse
from alive_progress import alive_bar


parser = argparse.ArgumentParser(description='Create a database from the crossref dump (already unzipped) with DOI and ISSN as colums')


parser.add_argument("--input",  required=True, type=str, help="Path of crossref dump unzipped")
parser.add_argument("--books", type=bool, default = False, help="Whether to include books or not")
parser.add_argument("--output", required=True, type=str, help="Path for the output results")

args = parser.parse_args()



def create_db(input_path, output_path, books = None):
    connection = sqlite3.connect(f"{output_path}/crossref_pulito.db")
    cursor = connection.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS articles (doi TEXT PRIMARY KEY, issn TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS books (doi TEXT PRIMARY KEY, issn TEXT)")
    connection.commit()
    
    with alive_bar(len(os.listdir(input_path))) as bar:
        connection = sqlite3.connect(f"{output_path}/crossref_pulito.db")
        cursor = connection.cursor()
        for el in os.listdir(input_path):
            to_clean = os.path.join(input_path, el)
            gzipped = to_clean
            f=gzip.open(gzipped,'rb')
            file_content= json.load(f)
            for record in file_content['items']:
                if 'ISSN' in record.keys():
                    doi = record['DOI']
                    issn = str(record['ISSN']).strip("']['")
                    cursor.execute("INSERT INTO articles VALUES (?, ?)", (doi, issn))
                elif 'ISBN' in record.keys() and books: # default è False
                    doi = record['DOI']
                    isbn = str(record['ISBN']).strip("']['")
                    cursor.execute("INSERT INTO books VALUES (?, ?)", (doi, isbn)) 
                else:
                    pass
            connection.commit()
            bar()
            
    cursor.close
    connection.close()
        
if __name__ == "__main__":
    create_db(args.input, args.output, args.books)
    print('done!')
