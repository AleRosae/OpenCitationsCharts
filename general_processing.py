import parse_COCI
import json
import sys
import pandas as pd

#run this script only when you update the general dataset
#It provides the .json files for the global statistics visualization

data = parse_COCI.load_data('prova_result_db.zip')
csvs = parse_COCI.load_csvs()
df = csvs['df_supergroups']
df["Description"] = [el.lower() for el in df['Description'].tolist()]
df.set_index('Description', inplace=True)


def get_general_processing(data, csvs, folder):
    print(f'Saving results in {folder}...')


    print('processing academic areas...')
    source_fields = parse_COCI.parse_data(data, csvs, asjc_fields=True)
    print(source_fields)
    for k in source_fields.keys():
        new_areas = []
        for key, value in source_fields[k].items():
            tmp = {}
            tmp['key'] = key
            tmp['data'] = value
            new_areas.append(tmp)
        source_fields[k] = new_areas 
    print('oooooiii')
    print(source_fields)
    new_groupssupergroups = []
    for area in source_fields['supergroups']:
        print("aoo")
        tmp = {}
        tmp['category'] = area['key']
        tmp['value'] = area['data']
        tmp['subData'] = []
        for field in source_fields['groups']:
            subtmp = {}
            print(area['key'], field['key'])
            if area['key'] == df.at[field['key'], 'Supergroup']:
                subtmp['category'] = field['key']
                subtmp['value'] = field['data']
                tmp['subData'].append(subtmp)

        if len(tmp['subData']) > 5:
            seg = tmp['subData'][:4]
            tot = sum([list(el.values())[1] for el in tmp['subData'][4:]])
            subtmp = {'category': "others", "value": tot}
            seg.append(subtmp)
            tmp['subData'] = seg
        new_groupssupergroups.append(tmp)

    source_fields['areas_GroupsAndSuper'] = new_groupssupergroups

    print('processing initial parsing...')
    init = parse_COCI.initial_parsing(data)
    init

    print('processing self citations by area...')
    d_self_citations_asjc = parse_COCI.self_citation(data, csvs, asjc_fields=True)
    new_selfcit= []
    for key, value in d_self_citations_asjc.items():
        tmp = {}
        tmp['key'] = key
        tmp['data'] = value
        new_selfcit.append(tmp)
    d_self_citations_asjc = new_selfcit  
        
    print('processing self citations by journals...')
    d_self_citations = parse_COCI.self_citation(data, csvs)
    new_selfcit= []
    for key, value in d_self_citations.items():
        tmp = {}
        tmp['key'] = key
        tmp['data'] = value
        new_selfcit.append(tmp)
    d_self_citations = new_selfcit  

    print('processing journals...')
    source_journals = parse_COCI.parse_data(data, csvs)
    new_journals = []
    for key, value in source_journals.items():
        tmp = {}
        tmp['key'] = key
        tmp['data'] = value
        new_journals.append(tmp)
    source_journals = new_journals

    print('processing network data...')
    net_data = parse_COCI.citations_networks(data)

    results = {'init': init, 'self_cit_area': d_self_citations_asjc, 'self_cit_journals': d_self_citations,
                'journals': source_journals, 'areas_fields': source_fields['fields'], 'areas_groups':source_fields['groups'],
                'areas_supergroups': source_fields['supergroups'], 'net': net_data, 'areas_GroupsAndSuper': source_fields['areas_GroupsAndSuper']}
    with open( folder + r'/final_results.json', 'w') as fp:
        json.dump(results, fp)

    print('Done!')

if __name__ == "__main__":
    get_general_processing(data, csvs, sys.argv[1])
    print('done!')

