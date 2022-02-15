from pandas.core.algorithms import mode
import streamlit as st
import json
import pandas as pd
from streamlit.type_util import Key
import parse_COCI
import numpy as np
from statistics import mean, mode
from zipfile import ZipFile
import plotly.express as px

st.set_page_config(page_title='OpenCitationsCharts', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items={
  'About': 'This app was developed for the epds course held by Prof. Marilena Daquino at the University of Bologna.'})
st.title('''OpenCitations in Charts''')
st.write('### A web application for visualizing the OpenCitations dataset in regards to publications distributed in 2020.')

@st.cache()
def load_data(path):
  with ZipFile(path, 'r') as zip:
    with zip.open('all_2020.json') as infile:
      d = json.load(infile)
      return d
if 'data' not in st.session_state:
  data = load_data(r'all_2020.zip')
  st.session_state['data'] = data
else:
  data = st.session_state['data']

@st.cache()
def load_csvs():
  csvs = parse_COCI.load_csvs()
  return csvs

if 'csvs' not in st.session_state:
  csvs = load_csvs()
  st.session_state['csvs'] = csvs
else:
  csvs = st.session_state['csvs']

if 'init' not in st.session_state:
  with open(r'results/initial.json', 'r') as j_file:
    init = json.load(j_file)
  st.session_state['init'] = init
else:
  init = st.session_state['init']

if 'self_citations_asjc' not in st.session_state:
  with open(r'results/d_self_citations_asjc.json', 'r') as j_file:
    d_self_citations_asjc = json.load(j_file)
  st.session_state['self_citations_asjc'] = d_self_citations_asjc
else:
  d_self_citations_asjc = st.session_state['self_citations_asjc']

if 'source_journals' not in st.session_state:
  with open(r'results/source_journals.json', 'r') as j_file:
    source_journals = json.load(j_file)
  st.session_state['source_journals'] = source_journals
else:
  source_journals = st.session_state['source_journals']

if 'source_fields' not in st.session_state:
  with open(r'results/source_fields.json', 'r') as j_file:
    source_fields = json.load(j_file)
  st.session_state['source_fields'] = source_fields
else:
  source_fields = st.session_state['source_fields']
  
if 'df_distribution' not in st.session_state:
  df_distribution = pd.DataFrame({'distribution (log scale)': init['tot_citations_distribution']})
  st.session_state['df_distribution'] = df_distribution
else:
  df_distribution = st.session_state['df_distribution']

if 'self_citations' not in st.session_state:
  with open(r'results/d_self_citations.json', 'r') as j_file:
    d_self_citations = json.load(j_file)
  st.session_state['self_citations'] = d_self_citations
else:
  d_self_citations = st.session_state['self_citations']

if 'net_data' not in st.session_state:
  with open(r'results/net_data.json', 'r') as j_file:
    d = json.load(j_file)
  net_data = parse_COCI.creat_vis_graph(d, tot=sum(init['tot_citations_distribution'])/1000)
  st.session_state['net_data'] = net_data
else:
  net_data = st.session_state['net_data']

initial_choice = st.sidebar.radio('What do you want to see?', ('General Statistics', 'Bibliometric Analysis'))
st.sidebar.markdown('***')
if initial_choice == 'General Statistics':
  state_exp=True
  general_stats = True
  with st.expander('OpenCitations in Charts', expanded=state_exp):
    st.write('''[OpenCitations](https://opencitations.net/) is an infrastructure organization for open scholarship dedicated to the publication 
            of open citation data as Linked Open Data. It provides bibliographic metadata of academic
            publications that are free to access, analyse and republish for any purpose. This web application aims at providing
            visualization of the COCI dataset created by OpenCitations and allows users to perform simple bibliometric analysis just by using
            the tools included in the left sidebar.''')
    st.write('''The **first time** you open the web page, Streamlit takes **a couple of minutes to load the dataset**. Grab a coffee in the meanwhile!
              By default the **main page** contains **statistics** about the whole COCI dataset, in particular its composition
              in terms of academic journals and subjects that are mentioned. This also serves as an example of the kind of analysis you can make with the 
              tools hereby provided. **Always check the top right corner of the screen**: when the running icon appears, it means that Streamlit is processing the data.
            You can use the **sidebar** to visualize **more specific data visualizations**, either using journals or academic fields
            as discriminators. Most of the charts are highly interactive, i.e. you can manipulate them to adjsut the scale, to zoom in or zoom out
            and you can always display them in full screen.''')
  with st.expander('How does it work?', expanded=state_exp):
    st.header('How does it work?')
    st.write('''You can perform two kinds of research. Either you can ask for **specific information about journals** related to a field or 
              you can **compare journals** belonging two different fields based on the discriminators that you choose. For instance, you can confront
              journals of biology and philosophical journals in regards to how they tend to mention journals belonging to their own field. Or you can simply
              retrive the most mentioned journals in general medicine. The names of the fields that can be used to perform the analysis 
              are those provided by the All Science Journal Classification (ASJC), which you can always consult [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).
              For istance, if you want to search for medical journals, you might want to search for "General Medicine", instead of just typying "Medicine".
              The input boxes are case insensitive and if you make some mistakes or you submit a field that does not belong to the ASJC codes the system will automatically inform you and suggest you
              possible solutions.''')
    st.write('''Currently the application **provides information about a sample of the publications released in 2020** (you can find more information about how the
            data was parsed, processed and created starting from the COCI dataset in the [GitHub repository](https://github.com/AleRosae/OpenCitationsCharts) of the application). 
            It is meant to represent a small glimpse of how 2020 went in terms of academic publications, finding an answer to research questions such as:
            which were the most influencing journals? Which were the most important themes covered by them? 
            Additionaly, since all the data comes from an Open Science project, it also gives an idea of which are the academic branches 
            and the scientific journals that are more prone to comply with the Open Science principles.''')

  col7, col8 = st.columns([3, 1])
  st.sidebar.write('''The charts that were drawn in the main page display information about the general composition of the COCI dataset
           in regards to the publications that appeared throughtout 2020.''')
  st.sidebar.write('''If you want to perform bibliometric analysis on the fly just check the 'Bibliometric analysis' box and fill all 
                   the input fields. Your results will appear on the main page.''')
  
else:
  state_exp=False
  general_stats = False
  with st.expander('OpenCitations in Charts', expanded=state_exp):
    st.write('''[OpenCitations](https://opencitations.net/) is an infrastructure organization for open scholarship dedicated to the publication 
            of open citation data as Linked Open Data. It provides bibliographic metadata of academic
            publications that are free to access, analyse and republish for any purpose. This web application aims at providing
            visualization of the COCI dataset created by OpenCitations and allows users to perform simple bibliometric analysis just by using
            the tools included in the left sidebar.''')
    st.write('''The **first time** you open the web page, Streamlit takes **a couple of minutes to load the dataset**. Grab a coffee in the meanwhile!
              By default the **main page** contains **statistics** about the whole COCI dataset, in particular its composition
              in terms of academic journals and subjects that are mentioned. This also serves as an example of the kind of analysis you can make with the 
              tools hereby provided. **Always check the top right corner of the screen**: when the running icon appears, it means that Streamlit is processing the data.
            You can use the **sidebar** to visualize **more specific data visualizations**, either using journals or academic fields
            as discriminators. Most of the charts are highly interactive, i.e. you can manipulate them to adjsut the scale, to zoom in or zoom out
            and you can always display them in full screen.''')
  with st.expander('How does it work?', expanded=state_exp):
    st.header('How does it work?')
    st.write('''You can perform two kinds of research. Either you can ask for **specific information about journals** related to a field or 
              you can **compare journals** belonging two different fields based on the discriminators that you choose. For instance, you can confront
              journals of biology and philosophical journals in regards to how they tend to mention journals belonging to their own field. Or you can simply
              retrive the most mentioned journals in general medicine. The names of the fields that can be used to perform the analysis 
              are those provided by the All Science Journal Classification (ASJC), which you can always consult [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).
              For istance, if you want to search for medical journals, you might want to search for "General Medicine", instead of just typying "Medicine".
              The input boxes are case insensitive and if you make some mistakes or you submit a field that does not belong to the ASJC codes the system will automatically inform you and suggest you
              possible solutions.''')
    st.write('''Currently the application **provides information about a sample of the publications released in 2020** (you can find more information about how the
            data was parsed, processed and created starting from the COCI dataset in the [GitHub repository](https://github.com/AleRosae/OpenCitationsCharts) of the application). 
            It is meant to represent a small glimpse of how 2020 went in terms of academic publications, finding an answer to research questions such as:
            which were the most influencing journals? Which were the most important themes covered by them? 
            Additionaly, since all the data comes from an Open Science project, it also gives an idea of which are the academic branches 
            and the scientific journals that are more prone to comply with the Open Science principles.''')
  col7, col8 = st.columns([3, 1])

  st.sidebar.write('''Choose between one single input query or multiple inputs analysis, fill the text boxes
                    and then **press Go**.''')
  search_choice = st.sidebar.radio('', ('Single field', 'Multiple fields'))
  if search_choice == 'Single field':
    single_search = st.sidebar.radio(
        "What do you want to search for?",
        ('Top journals cited by a field', 'Top journals cited by another journal','Self citations of a field', 'Citations flow'))
    if single_search == 'Top journals cited by a field':
      st.sidebar.write('Retrieve the top k journals belonging to a **specific field** according to how much they were cited.')
      input_field = st.sidebar.text_input('Journal field', '', key=1234, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                            You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''',
                                            placeholder='e.g. philosophy')
      n_items = st.sidebar.slider('number of journals', 1, 20, 10)
    elif single_search == 'Top journals cited by another journal':
      st.sidebar.write('Retrieve the top k journals that received more citations from a **specific journal** (except itself!).')
      input_field = st.sidebar.text_input('Journal name', '', key=12335464, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                            You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''',
                                            placeholder='e.g. The Lancet')
      n_items = st.sidebar.slider('number of journals', 1, 20, 10)
    elif single_search == 'Self citations of a field':
      st.sidebar.write('''Display how much journals belonging to a **specific field** tend to mentioned journals that belongs to their
       own field/group/subject area (this may take a couple of minutes to process).''')
      input_field = st.sidebar.text_input('Journal field', '', key=123, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                                You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''',
                                                placeholder='e.g. philosophy')
    elif single_search == 'Citations flow':
      st.sidebar.write('''Starting from a **specific field**, display which are the other most cited fields by it. ''')
      input_field = st.sidebar.text_input('Journal field', '', key=1122, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                                You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''',
                                                placeholder='e.g. philosophy')
    button = st.sidebar.button('Go', key= 91239)
    if button and input_field != '' and single_search == 'Top journals cited by a field':
      result_mistakes = parse_COCI.spelling_mistakes(input_field)
      if result_mistakes == False:
        result = parse_COCI.parse_data(data, csvs, asjc_fields = True, specific_field=input_field)
        with col8:
          st.markdown('***')
          if sum(list(result[input_field].values())) > round(np.mean(list(source_fields['fields'].values()))):
            st.write(f'''In the COCI dataset there are **{str(len(result[input_field].keys()))} journals** related to **{input_field}**,
             for a total of **{str(sum(result[input_field].values()))} citations**.
            This is higher than the average number of citations for a single field ({round(np.mean(list(source_fields['fields'].values())))}).''')
          else:
            st.write(f'''There are **{str(len(result[input_field].keys()))} journals** related to **{input_field}**, for a total of **{str(sum(result[input_field].values()))} citations**.
            This is below the average number of citations for a single field ({round(np.mean(list(source_fields['fields'].values())))}).''')
          st.write(f'''The most important journal is _{list(result[input_field].keys())[0]}_, which received {list(result[input_field].values())[0]} citations.
          The journal with less citations is _{list(result[input_field].keys())[-1]}_, which was mentioned only {list(result[input_field].values())[-1]} times.''')   
          st.write(f'''The average number of citations for each journal of {input_field} is around {round(mean(result[input_field].values()))}.''') 
        with col7:
          st.header(f'The most cited journals of {input_field}')
          source = pd.DataFrame({'journals': list(result[input_field].keys())[:n_items], 'number of citations': list(result[input_field].values())[:n_items]})
          bars = px.bar(source, y="number of citations", x="journals", color='number of citations', orientation='v',
                        color_continuous_scale='purples',  color_continuous_midpoint=list(result[input_field].values())[3], height=700)
          bars.update_layout(
            title = {'text':f'<b>Top {n_items} journals of {input_field}</b>',
            'xanchor':'center',
            'x': 0.5}
          )
          bars.update_coloraxes(showscale=False)
          st.plotly_chart(bars, use_container_width=True)
          top_journal = list(result[input_field].keys())[0]
          st.header(f'What do we know about {top_journal}?')
          st.write(f'''You might be interested in knowing something more about the most cited journal of {input_field}.
                    Here you can see some information about it, provided that the 
                    there are records of the journal in the COCI dataset. If you are interested in another journal, you can always perform
                    the same search with the related tool in the left sidebar.''')
        col13, col14 = st.columns([3, 1])
        with col13:
          result_journal = parse_COCI.search_specific_journal(data, csvs, specific_journal=top_journal)
          if top_journal not in result_journal.keys():
              st.header('Journal not found!')
              st.write('''It looks like the journal you searched did not make any citation in 2020 according to the COCI dataset.
                        This is probabily due to the fact that the Streamlit application is currently running on a partial subset of
                        the 2020 data, which is in turn a small subset of the whole COCI dataset.
                        Or maybe we need to open a little bit more this particular branch of science :)''')
              st.markdown('***')
          else:
            source = pd.DataFrame({'journals': list(result_journal[top_journal]['citations'].keys())[:10], 
                                   'number of citations': list(result_journal[top_journal]['citations'].values())[:10]})
            bars = px.bar(source, y="number of citations", x="journals", color='number of citations', orientation='v',
                          color_continuous_scale='purples',  color_continuous_midpoint=list(result_journal[top_journal]['citations'].values())[3], height=800)
            bars.update_layout(
              title={
                'text': f'<b>The journals that are cited the most by {top_journal.capitalize()}</b>',
                'x':0.5,
                'xanchor':'center'
              }
            )
            bars.update_coloraxes(showscale=False)
            st.plotly_chart(bars, use_container_width=True)
            st.markdown('***')
          if top_journal not in result_journal.keys():
            pass
          else:
            with col14:
              st.markdown('***')
              st.write(f'''The bar chart displays which are the journals that received most citations from _{top_journal.capitalize()}_, 
                          giving us the general idea of where it is most likely to find articles related to the same topic.''')
              st.write(f'''_{top_journal.capitalize()}_ is a journal of {result_journal[top_journal]['field']}, which belongs to the
                          {result_journal[top_journal]['group']} group.''')
              st.write(f'''{len(list(result_journal[top_journal]['citations'].keys()))} unique journals have been cited by _{top_journal}_ for a total
                      of {sum(list(result_journal[top_journal]['citations'].values()))} citations.
                      The journal that has been cited the most by _{top_journal}_ is _{list(result_journal[top_journal]['citations'].keys())[0]}_ with
                      {list(result_journal[top_journal]['citations'].values())[0]} mentions. ''')  
      elif result_mistakes == None:
        st.sidebar.write(f"Can't find {input_field}. Check the spelling")
      else:
        result_mistakes = str(result_mistakes[input_field]).strip('][')
        st.sidebar.write(f"Can't find {input_field}. Did you mean one of the following: {result_mistakes} ?")
        
    elif button and input_field != "" and single_search == 'Top journals cited by another journal':
      result_mistakes = parse_COCI.spelling_mistakes(input_field, journal=True)
      if result_mistakes == False:
        result = parse_COCI.search_specific_journal(data, csvs, specific_journal=input_field)
        if len(result) == 0:
          with col8:
            st.header('Journal not found!')
            st.write('''It looks like the journal you searched did not make any citation in 2020 according to the COCI dataset.
                      This is probabily due to the fact that the Streamlit application is currently running on a partial subset of
                      the 2020 data, which is in turn a small subset of the whole COCI dataset.
                      Or maybe we need to open a little bit more this particular branch of science :)''')
        else:
          with col8:
            st.markdown('***')
            st.write(f'''The bar chart displays which are the journals that received more citations from _{input_field.capitalize()}_, 
                          giving us the general idea of where it is most likely to find articles related to the same topic.''')
            st.write(f'''_{input_field.capitalize()}_ is a journal of {result[input_field]['field']}, which belongs to the
                        {result[input_field]['group']} group.''')
            st.write(f'''{len(list(result[input_field]['citations'].keys()))} unique journals have been cited by _{input_field}_ for a total
                    of {sum(list(result[input_field]['citations'].values()))} citations.
                    The journal that has been cited the most by _{input_field.capitalize()}_ is _{list(result[input_field]['citations'].keys())[0]}_ with
                    {list(result[input_field]['citations'].values())[0]} mentions. ''')
          with col7:
            st.header(f'The journals that are cited the most by {input_field.capitalize()}')
            source = pd.DataFrame({'journals': list(result[input_field]['citations'].keys())[:n_items], 'number of citations': list(result[input_field]['citations'].values())[:n_items]})
            bars = px.bar(source, y="number of citations", x="journals", color='number of citations', orientation='v',
                          color_continuous_scale='purples',  color_continuous_midpoint=list(result[input_field]['citations'].values())[3], height=800)
            bars.update_layout(title={
              'text': f'<b>Top {n_items} journals cited by {input_field.capitalize()}</b>',
              'x': 0.5,
              'xanchor': 'center'
            })
            bars.update_coloraxes(showscale=False)
            st.plotly_chart(bars, use_container_width=True)

          top_journal = list(result[input_field]['citations'].keys())[0]
          st.header(f'What do we know about {top_journal}?')
          st.write(f'''You might be interested in knowing something more about the most cited journal of {input_field}.
                    Here you can see some information about it, provided that the 
                    there are records of the journal in the COCI dataset. If you are interested in another journal, you can always perform
                    the same search with the related tool in the left sidebar.''')
        col13, col14 = st.columns([3, 1])
        with col13:
          result_journal = parse_COCI.search_specific_journal(data, csvs, specific_journal=top_journal)
          if top_journal not in result_journal.keys():
              st.header('Journal not found!')
              st.write('''It looks like the journal you searched did not make any citation in 2020 according to the COCI dataset.
                        This is probabily due to the fact that the Streamlit application is currently running on a partial subset of
                        the 2020 data, which is in turn a small subset of the whole COCI dataset.
                        Or maybe we need to open a little bit more this particular branch of science :)''')
              st.markdown('***')
          else:
            source = pd.DataFrame({'journals': list(result_journal[top_journal]['citations'].keys())[:10], 
                                   'number of citations': list(result_journal[top_journal]['citations'].values())[:10]})
            bars = px.bar(source, y="number of citations", x="journals", color='number of citations', orientation='v',
                          color_continuous_scale='purples',  color_continuous_midpoint=list(result_journal[top_journal]['citations'].values())[3], height=800)
            bars.update_layout(title={
              'text': f'<b>Top journals cited by {top_journal.capitalize()}</b>',
              'x': 0.5,
              'xanchor': 'center'
            })
            bars.update_coloraxes(showscale=False)
            st.plotly_chart(bars, use_container_width=True)
            st.markdown('***')
          if top_journal not in result_journal.keys():
            pass
          else:
            with col14:
              st.markdown('***')
              st.write(f'''The bar chart displays which are the journals that received most citations from _{top_journal.capitalize()}_, 
                          giving us the general idea of where it is most likely to find articles related to the same topic.''')
              st.write(f'''_{top_journal.capitalize()}_ is a journal of {result_journal[top_journal]['field']}, which belongs to the
                          {result_journal[top_journal]['group']} group.''')
              st.write(f'''{len(list(result_journal[top_journal]['citations'].keys()))} unique journals have been cited by _{top_journal}_ for a total
                      of {sum(list(result_journal[top_journal]['citations'].values()))} citations.
                      The journal that has been cited the most by _{top_journal}_ is _{list(result_journal[top_journal]['citations'].keys())[0]}_ with
                      {list(result_journal[top_journal]['citations'].values())[0]} mentions. ''')  
      elif result_mistakes == None:
        st.sidebar.write(f"Can't find {input_field}. Check the spelling")
      else:
        result_mistakes = str(result_mistakes[input_field]).strip('][')
        st.sidebar.write(f"Can't find {input_field}. Did you mean one of the following: {result_mistakes} ?")
      
    elif button and input_field != "" and single_search == 'Self citations of a field':
      check_spelling_selfcit = parse_COCI.spelling_mistakes(input_field)
      if check_spelling_selfcit == False:
        self_citation_field = parse_COCI.self_citation(data, csvs, asjc_fields=True, specific_field=input_field)
        df_selfcit = pd.DataFrame({'fields': self_citation_field.keys(), 'values': self_citation_field.values()})
        with col7:
          st.header(f'Self citations of {input_field}')
          fig = px.pie(df_selfcit, values='values', names='fields', color_discrete_sequence=['#00CC96', '#636EFA', '#EF553B'])
          st.plotly_chart(fig, use_container_width=True) 
        with col8:
          st.markdown('***')
          st.write(f'''The pie chart displays how many articles related to **{input_field}** tend to mention
                    articles related to the same field. It is a rough discriminator of how much a field tend to cross its disciplinary boundaries
                    relying also on external subjects. Self citations are scored when an article mentions another article belonging to
                    the same exact ASJC code, while partial self citations include articles that are not the exact match but
                    that belong to the same ASJC group.''')
          st.write(f'''In **{input_field}** there are **{df_selfcit.iloc[0,1]} self citations**,
          **{df_selfcit.iloc[1,1]} partial self-citations** 
          and **{df_selfcit.iloc[2,1]} not self citations**.''')
        st.markdown('***')
      elif check_spelling_selfcit == None:
        st.sidebar.write(f"Can't find {input_field}. Check the spelling.")
      else:
        check_spelling_selfcit = str(check_spelling_selfcit[input_field]).strip('][')
        st.sidebar.write(f"Can't find {input_field}. Did you mean one of the following: {check_spelling_selfcit} ?")

    elif button and  input_field != '' and single_search == 'Citations flow':
      check_spelling_selfcit = parse_COCI.spelling_mistakes(input_field)
      if check_spelling_selfcit == False:
        st.header(f'Citations flow in {input_field}')
        st.write(f'''The charts below display **how citations have flowed** starting from journals related to **{input_field}**. It is a general ovwerview of how different
                    academic fields interact with each other, using citations as a proxy for linking two different fields.''')
        col7, col8 = st.columns(2)
        source_citflow = parse_COCI.citations_flow(data, csvs, specific_field=input_field)
        df_citflow = pd.DataFrame({'fields': list(source_citflow['fields'].keys())[:10], 'number of citations': list(source_citflow['fields'].values())[:10]})

        with col7:
          bars = px.bar(df_citflow, y="number of citations", x="fields", color='number of citations', orientation='v',
                          color_continuous_scale='blues',  color_continuous_midpoint=list(source_citflow['fields'].values())[3], height=800)
          bars.update_layout(title={
            'text': f'<b>Fields mentioned more often by {input_field}</b>',
            'x': 0.5,
            'xanchor': 'center'
          })
          bars.update_coloraxes(showscale=False)
          st.plotly_chart(bars, use_container_width=True)
        with col8:
          tot_cit_supergroups = sum(source_citflow['supergroups'].values())
          df_cit_source_supergroups = pd.DataFrame({'supergroups': source_citflow['supergroups'].keys(), 
                                          'values': source_citflow['supergroups'].values()})
          fig = px.pie(df_cit_source_supergroups, values='values', names='supergroups', color_discrete_sequence=px.colors.qualitative.D3)
          fig.update_layout(title={
            'text': f'<b>Subject area of articles mentioned by {input_field}',
            'x': 0.5,
            'xanchor': 'center'
          })
          st.plotly_chart(fig, use_container_width=True) 
          
          #voglio solo i primi 10 categorie/valori, il resto va nella categoria others
          tot_cit_groups = sum(source_citflow['groups'].values())
          cit_groups_categories = [el[:20] for el in source_citflow['groups'].keys()][:12]
          cit_groups_values = list(source_citflow['groups'].values())[:12]
          cit_groups_others = sum(list(source_citflow['groups'].values())[12:])
          cit_groups_categories.append('Others')
          cit_groups_values.append(cit_groups_others)
          df_cit_source_groups = pd.DataFrame({'groups': cit_groups_categories, 
                                          'values': cit_groups_values})
          fig = px.pie(df_cit_source_groups, values='values', names='groups')
          fig.update_layout(title={
            'text': f'<b>Groups subdivision of articles mentioned by {input_field}',
            'x': 0.5,
            'xanchor': 'center'
          })
          st.plotly_chart(fig, use_container_width=True) 
        not_mentioned = str(parse_COCI.check_unmentioned(source_citflow['groups'])).strip('][')

        st.write(f'''The bar charts illustrates which are the other fields that are mostly citited by articles of **{input_field}**. This 
                  provides an idea of how these disciplines tend to communicate. In this case, the **most mentioned field is {list(source_citflow['fields'].keys())[0]}**,
                  with **{list(source_citflow['fields'].values())[0]} citations**. The **least one is {list(source_citflow['fields'].keys())[-1]}**, which apparently is the most distant
                  subject from {input_field}, with **only {list(source_citflow['fields'].values())[-1]} mentions**.''')
        st.write('''The pie charts on the right column illustrate the same values but plotted according to the **groups/subject area**
                  subdivision. ''')
        if len(not_mentioned) > 0:
          st.write(f'''The following groups were **never mentioned by {input_field}**: {not_mentioned}.''')
        else:
          st.write(f'''There is at least 1 citation from {input_field} in all the ASJC groups!''')
        st.markdown('***')

      elif check_spelling_selfcit == None:
        st.sidebar.write(f"Can't find {input_field}. Check the spelling.")
      else:
        check_spelling_selfcit = str(check_spelling_selfcit[input_field]).strip('][')
        st.sidebar.write(f"Can't find {input_field}. Did you mean one of the following: {check_spelling_selfcit} ?") 
        
  elif search_choice == 'Multiple fields':
    multiple_search = st.sidebar.radio(
        "What do you want to search for?",
        ('Number of citations per field', 'Self citations comparison', 'Citations flow comparison', 'Cross citations flow'))
    if multiple_search == 'Number of citations per field':
      st.sidebar.write('Display a comparison between **two or more different fields** according to the number of citations they received. Simply type a list of fields to compare them.')
      input_compare_field = st.sidebar.text_area('Fields (separated with comma and space)', '', key=4321, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                                You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''',
                                                placeholder='e.g. philosophy, general medicine, pharmacology')
      input_compare_field_cited = None
      button = st.sidebar.button('Go', key=7777)
    elif multiple_search == 'Self citations comparison':
      st.sidebar.write('''Display a comparison between **exactly two fields** in terms of how much they tend to mention disciplines belonging to their own field 
      (this may take a couple of minutes to process).''')
      input_compare_field = st.sidebar.text_input('Field 1', '', key=3342, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                                You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''',
                                                placeholder='e.g. philosophy')
      input_compare_field_cited = st.sidebar.text_input('Field 2', '', key=234235, help='''Fields must corrispond to ASJC fields (case insensitive). ''', 
                                                        placeholder='e.g. general medicine')
      button = st.sidebar.button('Go', key=8888)  
    elif multiple_search == 'Citations flow comparison':
      st.sidebar.write('''Display a comparison of the citations flow of **two different fields** i.e. which are the other fields that
                      received more citations from each of them (themselves excluded).''')
      input_compare_field= st.sidebar.text_input('Field 1', '', key=11223433, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                                You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''',
                                                placeholder='e.g. philosophy')
      input_compare_field_cited = st.sidebar.text_input('Field 2', '', key=234235, help='''Fields must corrispond to ASJC fields (case insensitive). ''',
                                                        placeholder='e.g. general medicine')
      button = st.sidebar.button('Go', key = 9988)

    elif multiple_search == 'Cross citations flow':
      st.sidebar.write('''Retrieve the journals of a specific field that are cited the most by journals of another particular field
                      (you might be particularly interested in fields fairly distant from each other).''')
      input_compare_field= st.sidebar.text_input('Field that is citing', '', key=12456, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                                You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''',
                                                placeholder='e.g. philosophy')
      input_compare_field_cited = st.sidebar.text_input('Field that received citations', '', key=12312, help='''Fields must corrispond to ASJC fields (case insensitive).
                                                        [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''',
                                                        placeholder='e.g. general medicine')
      button = st.sidebar.button('Go', key=9999)

    if input_compare_field != '' and multiple_search == 'Number of citations per field' and button: 
      render = True
      input = input_compare_field.split(', ')
      check_spelling = [parse_COCI.spelling_mistakes(inp) for inp in input]
      dict_spelling = [el for el in check_spelling if type(el) == dict]
      if None in check_spelling:
        index_cantfind = check_spelling.index(None)
        st.sidebar.write(f'''Can't find {input[index_cantfind]}. Check the spelling. Remember that you have to separte the fields only
                          with a comma and space, do not press enter!''')
        render = False
      elif len(dict_spelling)> 0:
        for dic in dict_spelling:
          for input_key, mistake_value in dic.items():
            mistake_value = str(mistake_value).strip('][')
            st.sidebar.write(f"Can't find {input_key}. Did you mean one of the following: {mistake_value} ?")
            render = False    
      else: 
        result = parse_COCI.parse_data(data, csvs, asjc_fields=True)['fields']
        output = {}
        result = {k.lower():v for k, v in result.items()}
        for item in input:
          output[item.capitalize()] = result[item.lower()]
      if render == True:
        st.header('Citations comparison by different fields')
        source = pd.DataFrame({'fields': output.keys(), 'number of citations': output.values()})
        bars = px.bar(source, y="number of citations", x="fields",  orientation='v',
                           height=700)
        bars.update_layout(title={
          'text': '<b>Number of citations comparison</b>',
          'x': 0.5,
          'xanchor': 'center'
        })
        bars.update_coloraxes(showscale=False)
        st.plotly_chart(bars, use_container_width=True)
        st.write('''The bar chart above compares the number of citation received by each field.''')
        st.markdown('***')

    elif input_compare_field != '' and input_compare_field_cited != '' and multiple_search == 'Self citations comparison' and button: 
      input = input_compare_field.strip() + ', ' + input_compare_field_cited.strip()
      input = input.split(', ')
      check_spelling = [parse_COCI.spelling_mistakes(inp) for inp in input]
      dict_spelling = [el for el in check_spelling if type(el) == dict]
      if None in check_spelling:
        index_cantfind = check_spelling.index(None)
        st.sidebar.write(f"Can't find {input[index_cantfind]}. Check the spelling")
      elif len(input) != 2:
        st.sidebar.write(f"You have to submit exactly 2 input here!")
      elif len(dict_spelling)> 0:
        for dic in dict_spelling:
          for input_key, mistake_value in dic.items():
            mistake_value = str(mistake_value).strip('][')
            st.sidebar.write(f"Can't find {input_key}. Did you mean one of the following: {mistake_value} ?")
      else: 
        col7, col8 = st.columns(2)
        self_citation_field_1 = parse_COCI.self_citation(data, csvs, asjc_fields=True, specific_field=input[0])
        df_selfcit_1 = pd.DataFrame({'fields': self_citation_field_1.keys(), 'values': self_citation_field_1.values()})
        self_citation_field_2 = parse_COCI.self_citation(data, csvs, asjc_fields=True, specific_field=input[1])
        df_selfcit_2 = pd.DataFrame({'fields': self_citation_field_2.keys(), 'values': self_citation_field_2.values()})
        st.header('Self citations comparison')
        st.write(f'''These pie charts **confront how many articles** related to **{input_compare_field}** or to **{input_compare_field_cited}** tend to mention
                    articles related to the **same field**. It is a rough discriminator of **how much a field tend to cross its disciplinary boundaries**
                    and cross with external subjects. Self citations are scored when an article mentions another article belonging to
                    the same exact ASJC code, while partial self citations includes articles that are not the exact match but
                    that belong to the same ASJC group. The comparison allows to detect substancial differences in the way in which fields belonging to different groups (e.g. medical sciences
                    and arts and humanities) tend to produce mentions related only to their own subject.''')
        with col7:
          st.write(f'''How many articles belonging to **{input_compare_field}** tend to mention
                    articles related to the same field.''')
          fig = px.pie(df_selfcit_1, values='values', names='fields', color_discrete_sequence=['#00CC96', '#636EFA', '#EF553B'])
          fig.update_layout(title={
            'text': f'<b>Self citations of {input[0]}</b>',
            'x': 0.5,
            'xanchor':'center'
          })
          st.plotly_chart(fig, use_container_width=True) 
          st.write(f'''In **{input_compare_field}** there are **{df_selfcit_1.iloc[0,1]} self citations**,
                    **{df_selfcit_1.iloc[1,1]} partial self-citations**
                    and **{df_selfcit_1.iloc[2,1]} not self citations**.''')
        with col8:
          st.write(f'''How many articles belonging to **{input_compare_field_cited}** tend to mention
                    articles related to the same field.''')
          fig = px.pie(df_selfcit_2, values='values', names='fields', color_discrete_sequence=['#00CC96', '#636EFA', '#EF553B'])
          fig.update_layout(title={
            'text': f'<b>Self citations of {input[1]}</b>',
            'x': 0.5,
            'xanchor':'center'
          })
          st.plotly_chart(fig, use_container_width=True) 
          st.write(f'''In **{input_compare_field_cited}** there are **{df_selfcit_2.iloc[0,1]} self citations**,
                    **{df_selfcit_2.iloc[1,1]} partial self-citations**
                    and **{df_selfcit_2.iloc[2,1]} not self citations**.''')

        st.markdown('***')
    elif input_compare_field != '' and input_compare_field_cited != '' and multiple_search == 'Citations flow comparison' and button: 
      col7, col8 = st.columns([2, 1])
      input = input_compare_field.strip() + ', ' + input_compare_field_cited.strip()
      input = input.split(', ')
      check_spelling = [parse_COCI.spelling_mistakes(inp) for inp in input]
      dict_spelling = [el for el in check_spelling if type(el) == dict]
      if None in check_spelling:
        index_cantfind = check_spelling.index(None)
        st.sidebar.write(f"Can't find {input[index_cantfind]}. Check the spelling")
      elif len(input) != 2:
        st.sidebar.write(f"You have to submit exactly 2 input here!")
      elif len(dict_spelling)> 0:
        for dic in dict_spelling:
          for input_key, mistake_value in dic.items():
            mistake_value = str(mistake_value).strip('][')
            st.sidebar.write(f"Can't find {input_key}. Did you mean one of the following: {mistake_value} ?")
      else:
        source_citflow_1 = parse_COCI.citations_flow(data, csvs, specific_field=input[0])
        source_citflow_2 = parse_COCI.citations_flow(data, csvs, specific_field=input[1])
        st.header(f'''Citations flow comparison between {input[0]} and {input[1]}''')
        st.write(f'''These pie charts below display the differences between how citations flow in {input[0].capitalize()} and in {input[1].capitalize()}, 
                according to their group and subject area.
                 This visualization gives us a general idea of where the citations made by journals belonging to those two fields are usually headed to.''')
        col7, col8 = st.columns(2)
        df_citflow_1 = pd.DataFrame({'fields': list(source_citflow_1['fields'].keys())[:10], 'values': list(source_citflow_1['fields'].values())[:10]})
        df_citflow_2 = pd.DataFrame({'fields': list(source_citflow_2['fields'].keys())[:10], 'values': list(source_citflow_2['fields'].values())[:10]})
        with col7:
          df_cit_source_supergroups_1 = pd.DataFrame({'supergroups': source_citflow_1['supergroups'].keys(), 
                                          'values': source_citflow_1['supergroups'].values()})
          st.header(f'{input[0].capitalize()}')
          fig = px.pie(df_cit_source_supergroups_1, values='values', names='supergroups', color_discrete_sequence=px.colors.qualitative.D3)
          fig.update_layout(title={
            'text': f'<b>Citations flow in {input[0]} (subject area)</b>',
            'x': 0.5,
            'xanchor':'center'
          })
          st.plotly_chart(fig, use_container_width=True) 
          #voglio solo i primi 10 categorie/valori, il resto va nella categoria others
          tot_cit_groups_1 = sum(source_citflow_1['groups'].values())
          cit_groups_categories_1 = [el[:20] for el in source_citflow_1['groups'].keys()][:12]
          cit_groups_values_1 = list(source_citflow_1['groups'].values())[:12]
          cit_groups_others_1 = sum(list(source_citflow_1['groups'].values())[12:])
          cit_groups_categories_1.append('Others')
          cit_groups_values_1.append(cit_groups_others_1)
          df_cit_source_groups_1 = pd.DataFrame({'groups': cit_groups_categories_1, 
                                          'values': cit_groups_values_1})
          fig = px.pie(df_cit_source_groups_1, values='values', names='groups')
          fig.update_layout(title={
            'text': f'<b>Citations flow in {input[0]} (groups)</b>',
            'x': 0.5,
            'xanchor':'center'
          })
          st.plotly_chart(fig, use_container_width=True) 
        with col8:
          st.header(f'{input[1].capitalize()}')
          df_cit_source_supergroups_2 = pd.DataFrame({'supergroups': source_citflow_2['supergroups'].keys(), 
                                          'values': source_citflow_2['supergroups'].values()})
          fig = px.pie(df_cit_source_supergroups_2, values='values', names='supergroups', color_discrete_sequence=px.colors.qualitative.D3)
          fig.update_layout(title={
            'text': f'<b>Citations flow in {input[1]} (subject area)</b>',
            'x': 0.5,
            'xanchor':'center'
          })
          st.plotly_chart(fig, use_container_width=True) 
          #voglio solo i primi 10 categorie/valori, il resto va nella categoria others
          cit_groups_categories_2 = [el[:20] for el in source_citflow_2['groups'].keys()][:10]
          cit_groups_values_2 = list(source_citflow_2['groups'].values())[:10]
          cit_groups_others_2 = sum(list(source_citflow_2['groups'].values())[10:])
          cit_groups_categories_2.append('Others')
          cit_groups_values_2.append(cit_groups_others_2)
          df_cit_source_groups_2 = pd.DataFrame({'groups': cit_groups_categories_2, 
                                          'values': cit_groups_values_2})
          fig = px.pie(df_cit_source_groups_2, values='values', names='groups')
          fig.update_layout(title={
            'text': f'<b>Citations flow in {input[0]} (groups)</b>',
            'x': 0.5,
            'xanchor':'center'
          })
          st.plotly_chart(fig, use_container_width=True) 
        set_1 = set(source_citflow_1['groups'].keys())
        set_2 = set(source_citflow_2['groups'].keys())
        set_merge = set_1.intersection(set_2)
        dict_merge = {k:source_citflow_1['groups'][k]+source_citflow_2['groups'][k] for k in set_merge}
        dict_merge = dict(sorted(dict_merge.items(), key=lambda item: item[1], reverse = True))
        keys_1 = [v for v in source_citflow_1['groups'].keys() if v in list(dict_merge.keys())[:10]]
        keys_2 = [v for v in source_citflow_2['groups'].keys() if v in list(dict_merge.keys())[:10]]
        values_1 = [source_citflow_1['groups'][v] for v in source_citflow_1['groups'].keys() if v in list(dict_merge.keys())[:10]]
        values_2 = [source_citflow_2['groups'][v] for v in source_citflow_2['groups'].keys() if v in list(dict_merge.keys())[:10]]
        df_citflow_merge = pd.DataFrame({'values':values_1+values_2, 'groups':keys_1+keys_2, 'field':[input[0] for i in range(len(keys_1))]+[input[1] for i in range(len(keys_2))]})
        st.write(f'''The bar chart below illustrates which are the disciplinary groups that both {input[0]} and {input[1]} tend to mention and their differences
                 in terms of absolute values. The groups that are mentioned by both fields were extracted and sorted considering the
                  sum of the citations of {input[0].capitalize()} and the citations of {input[1].capitalize()}.''')
        fig = px.histogram(df_citflow_merge, x="groups", y="values",
                    color='field', barmode='group',
                    histfunc='sum', height=800)
        fig.update_layout(title={
            'text': f'<b>Groups mentioned both by{input[0]} and {input[1]}',
            'x': 0.5,
            'xanchor':'center'
          })
        st.plotly_chart(fig, use_container_width=True)
      st.markdown('***')
    elif button and multiple_search == 'Cross citations flow' and input_compare_field != '' and input_compare_field_cited != '': 
      col7, col8 = st.columns([4, 1])
      input = input_compare_field.strip() + '; ' + input_compare_field_cited.strip()
      input = input.split('; ')
      check_spelling = [parse_COCI.spelling_mistakes(inp) for inp in input]
      dict_spelling = [el for el in check_spelling if type(el) == dict]
      if None in check_spelling:
        index_cantfind = check_spelling.index(None)
        st.sidebar.write(f"Can't find {input[index_cantfind]}. Check the spelling")
      elif len(input) != 2:
        st.sidebar.write(f"You have to submit exactly 2 input here!")
      elif len(dict_spelling)> 0:
        for dic in dict_spelling:
          for input_key, mistake_value in dic.items():
            mistake_value = str(mistake_value).strip('][')
            st.sidebar.write(f"Can't find {input_key}. Did you mean one of the following: {mistake_value} ?")
      else:
        source_citflow_journal = parse_COCI.citations_flow_journals(data, csvs, specific_fields=input)
        df_source_citflow_journal = pd.DataFrame({'journals': list(source_citflow_journal.keys())[:10], 
          'number of citations': list(source_citflow_journal.values())[:10]})
        with col7:
          st.header(f'Journals citations flow')
          bars = px.bar(df_source_citflow_journal, y="number of citations", x="journals", color='number of citations', orientation='v',
                        color_continuous_scale='blues', 
                         color_continuous_midpoint=list(source_citflow_journal.values())[int(len(source_citflow_journal.values())/3)], height=700)
          bars.update_layout(title={
            'text': f'<b>Journals citations flow</b>',
            'x': 0.5,
            'xanchor':'center'
          })
          bars.update_coloraxes(showscale=False)
          st.plotly_chart(bars, use_container_width=True)
        with col8:
          st.markdown("***")
          st.write(f'''The bar chart on the left displays the **main journals** related to **{input_compare_field_cited}** that have been
                **mentioned by** journals of **{input_compare_field}**.''')
          st.write(f'''The **most popular journal of {input_compare_field_cited}** among researchers of **{input_compare_field}** is 
                      _{list(source_citflow_journal.keys())[0]}_, with **{list(source_citflow_journal.values())[0]} mentions**.''')
          st.write(f'''**In total**, there are **{len(list(source_citflow_journal.keys()))} journals of {input_compare_field_cited}** that
                    have been cited by articles related to **{input_compare_field}**. The total number of citations received amount
                    to {sum(list(source_citflow_journal.values()))}.''')
        top_journal = list(source_citflow_journal.keys())[0]
        st.header(f'What do we know about {top_journal}?')
        st.write(f'''You might be interested in knowing something more about The **most popular journal 
                  of {input_compare_field_cited}** among researchers of **{input_compare_field}**.
                  Here you can see some information about it, provided that the 
                  there are records of the journal in the COCI dataset. If you are interested in another journal, you can always perform
                  the same search with the related tool in the left sidebar.''')
        col13, col14 = st.columns([3, 1])
        with col13:
          result_journal = parse_COCI.search_specific_journal(data, csvs, specific_journal=top_journal)
          if top_journal not in result_journal.keys():
              st.header('Journal not found!')
              st.write('''It looks like the journal you searched did not make any citation in 2020 according to the COCI dataset.
                        This is probabily due to the fact that the Streamlit application is currently running on a partial subset of
                        the 2020 data, which is in turn a small subset of the whole COCI dataset.
                        Or maybe we need to open a little bit more this particular branch of science :)''')
              st.markdown('***')
          else:
            source = pd.DataFrame({'journals': list(result_journal[top_journal]['citations'].keys())[:10], 
                                    'number of citations': list(result_journal[top_journal]['citations'].values())[:10]})
            bars = px.bar(source, y="number of citations", x="journals", color='number of citations', orientation='v',
                          color_continuous_scale='purples',  color_continuous_midpoint=list(result_journal[top_journal]['citations'].values())[3], height=800)
            bars.update_layout(title={
            'text': f'<b>The journals that are cited the most by {top_journal.capitalize()}</b>',
            'x': 0.5,
            'xanchor':'center'
          })
            bars.update_coloraxes(showscale=False)
            st.plotly_chart(bars, use_container_width=True)
            st.markdown('***')
          if top_journal not in result_journal.keys():
            pass
          else:
            with col14:
              st.write(f'''The bar chart displays which are the journals that received most citations from _{top_journal.capitalize()}_, 
                          giving us the general idea of where it is most likely to find articles related to the same topic.''')
              st.write(f'''_{top_journal.capitalize()}_ is a journal of {result_journal[top_journal]['field']}, which belongs to the
                          {result_journal[top_journal]['group']} group.''')
              st.write(f'''{len(list(result_journal[top_journal]['citations'].keys()))} unique journals have been cited by _{top_journal}_ for a total
                      of {sum(list(result_journal[top_journal]['citations'].values()))} citations.
                      The journal that has been cited the most by _{top_journal}_ is _{list(result_journal[top_journal]['citations'].keys())[0]}_ with
                      {list(result_journal[top_journal]['citations'].values())[0]} mentions. ''')  
      st.markdown('***')
if general_stats:
  st.header('General statistics')
  st.write('''This dashboard is meant to tell how 2020 went in terms of academic publication. You can visualize multiple statistics that were elaborated from the the 
           portion of COCI dataset that was pre-processed according to the constrains explaned in the introduction. Depending on the size of your screen, 
           you might want to minimize the left sidebar.''')   

  with st.expander('General statistics', expanded=True):
    st.write(f'''For the year 2020 the **COCI dataset** contains a **total of {sum(init['tot_citations_distribution'])} citations** that appeared in
              **{str(init['journals'])} unique journals**, which in total cover **{len(source_fields['fields'].keys())} different academic fields** that can be
              grouped by **{len(source_fields['groups'].keys())} different groups** according to the _All Science Journals Classification_ (**ASJC**).
              Here you can see which are the most cited journals and fields in the dataset throughout that year.''')
    col_char, col_text = st.columns([5, 1])
    with col_char:
      df_source_journals = pd.DataFrame({'journals': list(source_journals.keys())[:20], 'number of citations': list(source_journals.values())[:20]}) #prendo solo i primi 10
      bars = px.bar(df_source_journals, y="number of citations", x="journals", color='number of citations', orientation='v',
                    color_continuous_scale='purples',  color_continuous_midpoint=list(source_journals.values())[3], height=700)
      bars.update_layout(
              title={
              'text' :'<b>Top 20 journals by number of citations</b>',
              'x':0.5,
              'xanchor': 'center'})
      bars.update_coloraxes(showscale=False)
      st.plotly_chart(bars, use_container_width=True)
    with col_text:
      st.write('')
      st.write('')
      st.write('')
      st.write(f'''The chart displays the **journals that received the most number of citations** in 2020. It represents a rather simple overview of the most influencial
                scientific journals in 2020.''')
      st.write(f'''The **most cited journal** is _{list(source_journals.keys())[0]}_,
              with the astonishing number of **{list(source_journals.values())[0]} citations**. The **least cited journal** is _{list(source_journals.keys())[-1]}_,
              which received only {list(source_journals.values())[-1]} mentions.''')
    col_char, col_text = st.columns([5, 1])
    with col_char:
      df_source_fields = pd.DataFrame({'fields': list(source_fields['fields'].keys())[:20], 'number of citations': list(source_fields['fields'].values())[:20]})
      bars = px.bar(df_source_fields, y="number of citations", x="fields", color='number of citations', orientation='v',
                    color_continuous_scale='blues',  color_continuous_midpoint=list(source_fields['fields'].values())[3], height=700)
      bars.update_layout(
            title={
            'text' :'<b>Top 20 academic fields by number of citations</b>',
            'x':0.5,
            'xanchor': 'center'})
      bars.update_coloraxes(showscale=False)
      st.plotly_chart(bars, use_container_width=True)
    with col_text:
      st.write('')
      st.write('')
      st.write('')
      st.write(f'''The chart displays the **fields that received the most number of citations** in 2020. It represents the main themes and subjects that are 
              covered by the articles that were published in 2020.''')
      st.write(f'''The **most popular field** is **{list(source_fields['fields'].keys())[0]}**,
            with the astonishing number of **{list(source_fields['fields'].values())[0]} citations**. The least popular one is **{list(source_fields['fields'].keys())[-1]}**,
            which received only {list(source_fields['fields'].values())[-1]} mentions.''')
    
    histo_distr = px.histogram(df_distribution, x="distribution (log scale)",
                    log_x=True)
    histo_distr.update_layout(
      title={
        'text': '<b> Distribution of citations for article</b>',
        'x': 0.5,
        'xanchor': 'center'
      })
    st.plotly_chart(histo_distr, use_container_width=True)
    st.write(f'''**This chart displayes the distribution of the number of citations** of each citing article in 2020. On the x-axis you
            can find how many articles were mentioned (on a logarithmic scale), on the y-axis the number of instances of articles that cite n other articles.
            The distribution appears to be **very skewed**, with a large part of the articles mentioning few publiscations and a very few other articles
            citing hundred or thousands of other publications. It might be the case that the latter represents meta-reviews or a general overview
            of the current literature available for a specific topic.''')
    st.write(f'''The **average number of citations** for citing articles in 2020 was **{init['average_citations']}**, the mode (i.e. the most frequent value)
            was **{mode(init['tot_citations_distribution'])}**, which implies a very skewed distribution.
            The **maximum number of mentions** was **{max(init['tot_citations_distribution'])}**, while the **minimum was {min(init['tot_citations_distribution'])}**.''')
  with st.expander('Fields subdivision', expanded=True):
    st.write('''The bar chart above displays the **most important fields** in 2020, i.e. those that received more citations. 
            However, **ASJC** also comes with a subdivion of those fields in
            more general groups that give us a general picture of the subjects that are covered. The pie charts offer a broader look at the composition
            of the COCI dataset by illustrating the same data grouped according to the **group subdivision** and their **relative subject area** (i.e. the most general
            subdivision possible).''')
    df_source_groups = pd.DataFrame({'groups': list(source_fields['groups'].keys()), 'number of citations': list(source_fields['groups'].values())})
    bars = px.bar(df_source_groups, y="number of citations", x="groups", color='number of citations', orientation='v',
                    color_continuous_scale='blues',  color_continuous_midpoint=list(source_fields['groups'].values())[3], height=700)
    bars.update_coloraxes(showscale=False)
    bars.update_layout(
      title={
        'text': '<b>Academic groups by number of citations</b>',
        'x': 0.5,
        'xanchor': 'center'
      })
    st.plotly_chart(bars, use_container_width=True)
    col9, col10 = st.columns(2)
    with col9:
      tot_groups = sum(source_fields['groups'].values())
      groups_categories = [el[:20] for el in source_fields['groups'].keys()][:15]
      groups_values = list(source_fields['groups'].values())[:15]
      groups_others = sum(list(source_fields['groups'].values())[15:])
      groups_categories.append('Others')
      groups_values.append(groups_others)
      df_source_groups = pd.DataFrame({'groups': groups_categories, 
                                      'values': groups_values})
      fig = px.pie(df_source_groups, values='values', names='groups')
      fig.update_layout(
      title={
        'text': '<b>Academic groups subdivision</b>',
        'x': 0.4,
        'xanchor': 'center'
      })
      st.plotly_chart(fig, use_container_width=True)  
      st.write(f'''The **subdivision** of the {len(source_fields['fields'].keys())} fields present in the COCI dataset in **groups**. The **most popular group**
              is **{list(source_fields['groups'].keys())[0]}** which received **{list(source_fields['groups'].values())[0]} mentions**. The least popular one is 
              {list(source_fields['groups'].keys())[-1]} with {list(source_fields['groups'].values())[-1]} citations. 
              _Others_ include: {str(list(source_fields['groups'].keys())[15:]).strip('][')}.''')
      with col10:
        df_source_supergroups = pd.DataFrame({'supergroups': source_fields['supergroups'].keys(), 
                                        'values': source_fields['supergroups'].values()})
        fig = px.pie(df_source_supergroups, values='values', names='supergroups', color_discrete_sequence=px.colors.qualitative.D3)
        fig.update_layout(
        title={
        'text': '<b>Academic subject area subdivision</b>',
        'x': 0.4,
        'xanchor': 'center'
      })
        st.plotly_chart(fig, use_container_width=True) 
        st.write(f'''The **subdivision** of the {len(source_fields['groups'].keys())} groups present in the COCI dataset according to subject areas. The **most popular subject area** is
              **{list(source_fields['supergroups'].keys())[0]}** which received **{list(source_fields['supergroups'].values())[0]} mentions**. The least popular one is 
              {list(source_fields['supergroups'].keys())[-1]} with {list(source_fields['supergroups'].values())[-1]} citations.''')

  with st.expander("Citations flow", expanded=True):
    st.write('''Where did citations exactly went throughout 2020? This section offers a general overview of the network created by the scientific
            publications according to their group subdivision. Moreover, it display how much journals of the same field tend to mention articles
            belonging to other fields.
            This is particularly interesting because it gives us an idea of how much the journals in the dataset are
            **cross-disciplinary**. With the sidebar you can also see statistics related to one specific field in order to see which are the subject that are more 
            prone to cross the boundaries between different fields. ''')
    st.plotly_chart(net_data, use_container_width=True)
    st.write('''This is a simple yet effective visualization of the networks
    created by the citations of the 27 groups present the COCI dataset for 2020. Edges thickness is defined by the number of connections between two nodes,
    while the size of each node depends by its own degree i.e. the total number of connections (in and out). The position of the nodes
    was layed out using the [Fruchterman-Reingold force-directed algorithm](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html).''')
    col1, col2 = st.columns(2)
    with col2:
      df_d = pd.DataFrame({'category': d_self_citations.keys(), 'values': d_self_citations.values()})
      fig = px.pie(df_d, values='values', names='category', color_discrete_sequence=['#636EFA', '#EF553B'])
      fig.update_layout(
        title={
        'text': '<b>Self citations (by journals)</b>',
        'x': 0.5,
        'xanchor': 'center'
      })
      st.plotly_chart(fig, use_container_width=True) 
      st.write('Articles that mention publications that belong to the same journal of the citing article.')
    with col1:
      df_d_asjc = pd.DataFrame({'category': d_self_citations_asjc.keys(), 'values': d_self_citations_asjc.values()})
      fig = px.pie(df_d_asjc, values='values', names='category', color_discrete_sequence=['#00CC96', '#636EFA', '#EF553B'])
      fig.update_layout(
        title={
        'text': '<b>Self citations (by field)</b>',
        'x': 0.5,
        'xanchor': 'center'
      })
      st.plotly_chart(fig, use_container_width=True) 
      st.write('''Articles that mention publications belonging to the same academic field or of similar academic field (according to ASJC classification).
      Self citations are scored when an article mentions another article belonging to the same exact ASJC code, 
      while partial self citations include articles that are not the exact match but that belong to the same ASJC group.''')
  