# OpenCitationsCharts
Repository for a web application that displays statistics about the OpenCitations COCI dataset. Currently the application works only on a subset of the COCI dataset which includes only citations made during year 2020. It is meant as a project for the final examination of the Electronic Publishing and Digital Storytelling course held by Prof. Marilena Daquino at the University of Bologna in the Digital Humanities and Digital Knowledge master's degree. 

# How does it work
In order to build the application the following steps were made:
<ul>
<li>Gather the COCI dump from the OpenCitations website and the Crossref dump at the Crossref website.</li>
<li>Clean the Crossref dump locally, keeping only info about the ISSN code of each DOI </li>
<li>Compute the interaction between each journal, i.e. count how many times journal A mentions journals X, Y, Z</li>
<li>Use the All Science Journals Classification codes for transforming ISSN into journals and/or academic fields</li>
<li>Use the results of the computation to display statistics and perform bibiometric analysis in the Streamlit application</li>
</ul>

The Google Colab notebooks in the Notebooks folder were made to process and parse the dataset. Note that some of the computation were made locally, so they cannot be run with the hosted connection. Further details and instructions cab be found in the notebooks.
Currently the streamlit application works in a hybrid way: the global statistics were pre-processed and stored as .json files in the results folder, which are used to display general information about the COCI dataset in the main page. The bibliometric analysis are computed in real time, using the dataset that loads when the application is run for the first time. This approach currently works well for the 2020 COCI subset, but it cannot be reproduced for the whole dataset. In this case, a proper database storing all the possible computations may be implemented. 

# What can you do with the application
In addition to serve as a general display of the content of the COCI dataset, the web application is meant to perform some simple yet interesting bibliometric analysis on the fly. The left side-bar can be used to switch from the global visualization to the bibliometric tools, allowing for two kinds of query: a single field search, with which users can retrieve different information about one specific field or one specifi journal, and a multi fields comparison, that allows to compare different fields. Additionally, the latter allows for more sophisticated queries: for istance, it is possible to retrieve the journals of a specific field (e.g. philosophy) that are cited the most exclusively by journals of another field (e.g. medicine). 

You can check the Streamlit demo here: https://share.streamlit.io/alerosae/opencitationscharts/epds-exam/app.py
