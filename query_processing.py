import parse_COCI
import json
import sys
from alive_progress import alive_bar
import time

#run this script only when you update the general dataset
#It provides the .json files for the global statistics visualization

data = parse_COCI.load_data('all_2020.zip')
csvs = parse_COCI.load_csvs()

def get_single_field_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')
    fields = csvs['df_asjc']['Description'].tolist()
    fields = fields
    results = {}
    print('processing most cited by single field...')
    with alive_bar(len(fields)) as bar:
        for input_field in fields:
            journals_cited_by_field = parse_COCI.parse_data(data, csvs, asjc_fields = True, specific_field=input_field)
            results[input_field] = journals_cited_by_field
            bar()
    with open( folder + r'/journals_cited_by_field_results.json', 'w') as fp:
        json.dump(results, fp)
    print('Done!')

if __name__ == "__main__":
    get_single_field_processing(data, csvs,  sys.argv[1])

