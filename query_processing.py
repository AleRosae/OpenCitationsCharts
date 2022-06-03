import parse_COCI
import json
from alive_progress import alive_bar
import argparse

parser = argparse.ArgumentParser(description='''Process the results of the computation in order to get general statistics related to all the specifc queries that can be
                                 performed on the Streamlit application. ''')

parser.add_argument("--data", required=True, type=str, help='''Data to process. It accepts a .json file in the format ISSN-a: {has_cited_n_times : {ISSN-b: 27, ISSN-c: 42}.
                                            Data can the either a plain .json or a zipped file containing that .json file.''')

parser.add_argument("--output", required=True, type=str, help="Path for the output results")

args = parser.parse_args()

def get_single_field_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')
    fields = csvs['df_asjc']['Description'].tolist()
    results = {}
    print('processing most cited by single field...')
    with alive_bar(len(fields)) as bar:
        for input_field in fields:
            journals_cited_by_field = parse_COCI.parse_data(data, csvs, asjc_fields = True, specific_field=input_field)
            results[input_field.lower()] = journals_cited_by_field
            bar()
    with open( folder + r'/journals_cited_by_field_results.json', 'w') as fp:
        json.dump(results, fp)
    print('Done!')

def get_single_journal_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')
    
    print('Processing most cited by single journal')
    results = parse_COCI.search_specific_journal(data, csvs)
    with open(folder + r'/journals_cited_by_journal_results.json', 'w') as fp:
        json.dump(results, fp)
    print('Done!')

def get_single_selfcitations_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')
    print('processing self-citations of a single field...')
    results = parse_COCI.query_self_citation(data, csvs)
    with open( folder + r'/self_citations_by_field_results.json', 'w') as fp:
        json.dump(results, fp)
    print('Done!')

def get_single_citationsflow_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')
    fields = csvs['df_asjc']['Description'].tolist()
    results = {}
    print('processing citations flow by field...')
    with alive_bar(len(fields)) as bar:
        for input_field in fields:
            source_citflow = parse_COCI.citations_flow(data, csvs, specific_field=input_field)
            results[input_field.lower()] = source_citflow
            bar()
    with open( folder + r'/citations_flow_by_field_results.json', 'w') as fp:
        json.dump(results, fp)
    print('Done!')


def get_cross_citationsflow_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')
    results = parse_COCI.citations_flow_journals(data, csvs)
    with open( folder + r'/cross_citations_flow_by_field_results.json', 'w') as fp:
        json.dump(results, fp)
    print('Done!')


def main(data, csvs, folder):

    get_cross_citationsflow_processing(data, csvs, folder)
    get_single_field_processing(data, csvs, folder)
    get_single_citationsflow_processing(data, csvs, folder)
    get_single_selfcitations_processing(data, csvs, folder)
    get_single_journal_processing(data, csvs, folder)


if __name__ == "__main__":
    if "zip" in args.data:
        data = parse_COCI.load_data(args.data)
    else:
        data = parse_COCI.load_data(args.data, zip=False)
        
    csvs = parse_COCI.load_csvs()
    
    main(data, csvs, args.output)
