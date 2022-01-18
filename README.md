# OpenCitationsCharts
Repository for the web application that displays statistics about the OpenCitations dataset. The web application is currently WIP and it might undergo significant changes during the development and/or some features might be broken. Performances are also not great and the first time users open the application it might take a couple of minutes to load the dataset and the global statistics. 

The parsing functions and the web app have been developed by using a rather small portion of the COCI dataset (i.e. file "020-04-25T04:48:36_1.csv"), which has been compressed in a .zip file to deal with GitHub files' size limits. 
The Crossref dataset has been cleaned to optmize the seach process. You can find more information about this on the notebooks that have run on Google Colab to process the data. 

You can check the Streamlit demo here: https://share.streamlit.io/alerosae/opencitationscharts/main
