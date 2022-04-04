import parse_COCI
import json
import sys

#run this script only when you update the general dataset
#It provides the .json files for the global statistics visualization

data = parse_COCI.load_data('prova_result_db.zip')
csvs = parse_COCI.load_csvs()


def get_general_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')

    print('processing initial parsing...')
    init = parse_COCI.initial_parsing(data)

    print('processing self citations by area...')
    d_self_citations_asjc = parse_COCI.self_citation(data, csvs, asjc_fields=True)
        
    print('processing self citations by journals...')
    d_self_citations = parse_COCI.self_citation(data, csvs)

    print('processing journals...')
    source_journals = parse_COCI.parse_data(data, csvs)

    print('processing academic areas...')
    source_fields = parse_COCI.parse_data(data, csvs, asjc_fields=True)

    print('processing network data...')
    net_data = parse_COCI.citations_networks(data)

    results = {'init': init, 'self_cit_area': d_self_citations_asjc, 'self_cit_journals': d_self_citations,
                'journals': source_journals, 'areas': source_fields, 'net': net_data}
    with open( folder + r'/final_results.json', 'w') as fp:
        json.dump(results, fp)

    print('Done!')

if __name__ == "__main__":
    get_general_processing(data, csvs, sys.argv[1])
    print('gephi data...')
    parse_COCI.create_gephi_data(sys.argv[1])
    print('done!')

