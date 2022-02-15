# OpenCitationsCharts
Repository for a web application that displays statistics about the OpenCitations COCI dataset. Currently the application is limited to a subset of the COCI dataset which includes only citations made during year 2020. It is meant as a project for the final examination of the Electronic Publishing and Digital Storytelling course held by Prof. Marilena Daquino at the University of Bologna in the Digital Humanities and Digital Knowledge master's degree. 
You can access the Streamlit application here: https://share.streamlit.io/alerosae/opencitationscharts/epds-exam/app.py


# Project workflow
In order to build the application the following steps were made:
<ul>
<li>Gather the COCI dump from the OpenCitations website and the Crossref dump at the Crossref website.</li>
<li>Clean the Crossref dump locally, keeping only info about the ISSN code of each DOI </li>
<li>Compute the interaction between each journal, i.e. count how many times journal A mentions journals X, Y, Z</li>
<li>Use the All Science Journals Classification codes for transforming ISSN into journals and/or academic fields</li>
<li>Use the results of the computation to display statistics and perform bibiometric analysis in the Streamlit application</li>
</ul>

The Google Colab notebooks in the Notebooks folder were made to process and parse the dataset. Note that some of the computation were made locally, so they cannot be run with the hosted connection. Further details and instructions about how data was parsed and processed can be found inside each notebook. 

# Data processing
The results of the processing operations is a .json file that representent the count of the citations according to the ISSN (the unique code associated with an academic journal) of both the citing and the cited article. Thus, a citation in the form of 'DOI_1 mentioned DOI_2' is transformed in 'ISSN_1 mentioned ISSN_2'. Then, a simple counting is performed to compute how many times each ISSN has mentioned another ISSN, creating a list of dictionaries that has the following structure:
'''issn: X, has_cited_n_times: {A: 30, B: 10, C: 1}'''
where X is the citing ISSN and A, B, C...N are the cited ISSN, each value of the key representing the number of times that X has mentioned N.

The results of the computation are than dumped in a .json file, zipped and loaded in the Streamlit application, which is composed of many functions able to work with the aforementioned data structure to retrieve the desidered output (e.g. the number of citations made by a specific journal). To access the proper titles and academic fields of each ISSN, the application relies on the Scopus dataset, which also includes the ASJC classification for every journal available. The original Excel file was parsed to extract journal titles, fields and groups subdivision and then converted into a more suitable .csv extension. 
# What can you do with the application
Currently the streamlit application works in a hybrid way: the global statistics were pre-processed and stored as .json files in the results folder, which are used to display general information about the COCI dataset in the main page. The bibliometric analysis are computed in real time, using the dataset that loads when the application is run for the first time. This approach currently works well for the 2020 COCI subset, but it cannot be reproduced for the whole dataset. In this case, a proper database storing all the possible computations may be implemented. 

In addition to serve as a general display of the content of the COCI dataset, the web application is meant to perform some simple yet interesting bibliometric analysis on the fly. The left side-bar can be used to switch from the global visualization to the bibliometric tools, allowing for two kinds of query: a single field search, with which users can retrieve different information about one specific field or one specifi journal, and a multi fields comparison, that allows to compare different fields. Additionally, the latter allows for more sophisticated queries: for istance, it is possible to retrieve the journals of a specific field (e.g. philosophy) that are cited the most exclusively by journals of another field (e.g. medicine). 

