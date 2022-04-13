import parse_COCI
import json
import sys
from alive_progress import alive_bar
import time


#run this script only when you update the general dataset
#It provides the .json files for the global statistics visualization


def get_single_field_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')
    fields = csvs['df_asjc']['Description'].tolist()[:10]
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

def get_single_journal_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')
    journals = csvs['df_issn']['Title'].tolist()[:10]
    results = {}
    print('Processing most cited by single journal')
    with alive_bar(len(journals)) as bar:
        for input_journal in journals:
            print(input_journal)
            journals_cited_by_journal = parse_COCI.search_specific_journal(data, csvs, specific_journal=input_journal)
            results[input_journal] = journals_cited_by_journal
            bar()
    with open(folder + r'/journals_cited_by_journal_results.json', 'w') as fp:
        json.dump(results, fp)
    print('Done!')

def get_single_selfcitations_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')
    fields = csvs['df_asjc']['Description'].tolist()[:10]
    results = {}
    print('processing self-citations of a single field...')
    with alive_bar(len(fields)) as bar:
        for input_field in fields:
            self_citation_field = parse_COCI.self_citation(data, csvs, asjc_fields=True, specific_field=input_field)
            results[input_field] = self_citation_field
            bar()
    with open( folder + r'/self_citations_by_field_results.json', 'w') as fp:
        json.dump(results, fp)
    print('Done!')

def get_single_citationsflow_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')
    fields = csvs['df_asjc']['Description'].tolist()[:10]
    results = {}
    print('processing citations flow by field...')
    with alive_bar(len(fields)) as bar:
        for input_field in fields:
            source_citflow = parse_COCI.citations_flow(data, csvs, specific_field=input_field)
            results[input_field] = source_citflow
            bar()
    with open( folder + r'/citations_flow_by_field_results.json', 'w') as fp:
        json.dump(results, fp)
    print('Done!')



def main(folder):
    data = parse_COCI.load_data('prova_result_db.zip') #the results of the first processing
    csvs = parse_COCI.load_csvs()
    #get_single_field_processing(data, csvs, folder)
    get_single_journal_processing(data, csvs, folder)
    get_single_citationsflow_processing(data, csvs, folder)
    get_single_selfcitations_processing(data, csvs, folder)


if __name__ == "__main__":
    main(sys.argv[1])
