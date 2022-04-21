import general_processing
import query_processing
import search_issn
import sys
import parse_COCI


if __name__ == "__main__":
    print("Processing COCI ->")
    search_issn.get_issn_crossref(sys.argv[1], sys.argv[2], sys.argv[3]) #coci folder, db path, results folder
    print("Starting general processing ->")
    general_processing.get_general_processing(data =  parse_COCI.load_data(sys.argv[3], zip=False), csvs=parse_COCI.load_csvs(), folder= sys.argv[3])
    print("Starting queries processing -> ")
    query_processing.main(data=parse_COCI.load_data(sys.argv[3], zip=False), csvs=parse_COCI.load_csvs(), folder=sys.argv[3])
    print('done!')