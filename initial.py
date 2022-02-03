import parse_COCI
import json

data = parse_COCI.load_data('all_2020.zip')
csvs = parse_COCI.load_csvs()


init = parse_COCI.initial_parsing(data)
with open(r'results/initial.json', 'w') as fp:
    json.dump(init, fp)

d_self_citations_asjc = parse_COCI.self_citation(data, csvs, asjc_fields=True)
with open(r'results/d_self_citations_asjc.json', 'w') as fp:
    json.dump(d_self_citations_asjc, fp)

source_journals = parse_COCI.parse_data(data, csvs)
with open(r'results/source_journals.json', 'w') as fp:
    json.dump(source_journals, fp)

source_fields = parse_COCI.parse_data(data, csvs, asjc_fields=True)
with open(r'results/source_fields.json', 'w') as fp:
    json.dump(source_fields, fp)

d_self_citations = parse_COCI.self_citation(data, csvs)
with open(r'results/d_self_citations.json','w') as fp:
    json.dump(d_self_citations, fp)

net_data = parse_COCI.citations_networks(data)
with open(r'results/net_data.json', 'w') as fp:
    json.dump(net_data, fp)