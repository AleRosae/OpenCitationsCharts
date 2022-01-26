from altair.vegalite.v4.schema.core import Align
from pandas.core.algorithms import mode
import streamlit as st
import re
import json
import streamlit.components.v1 as components
import pandas as pd
from streamlit.type_util import Key
import parse_COCI
import parse_initial
import numpy as np
import altair as alt
import scipy.stats as stats
from statistics import mean, mode
from zipfile import ZipFile

st.set_page_config(page_title='OpenCitationsCharts', page_icon=None, layout="wide", initial_sidebar_state="collapsed", menu_items={
  'About': 'This app was developed for the epds course held by Prof. Marilena Daquino at the University of Bologna.'})
st.write('''
         # OpenCitations in Charts
         ### A web application for visualizing the OpenCitations dataset.
         ''')
st.write('''[OpenCitations](https://opencitations.net/) is an infrastructure organization for open scholarship dedicated to the publication 
        of open citation data as Linked Open Data. It provides bibliographic metadata of academic
        publications that are free to access, analyse and republish for any purpose. Thsi web application aims at providing
        visualization of the COCI dataset of OpenCitations. Users are also allowed to perform simple bibliometrics analysis 
        using the research tools on the **left sidebar** (that you can open by clicking on the ">" symbol on the up-left corner of the page).''')
st.write('''The **first time** you open the web page, Streamlit takes **a couple of minutes to load the dataset**. Grab a coffee in the meanwhile!
          By default the **main page** contains **statistics** about the whole COCI dataset, in particular its composition
          in terms of academic journals and subjects that are mentioned.
         You can use the **sidebar** to visualize **more specific data visualizations**, either using journals or academic fields
         as discriminators. The charts you ask for will appear above the global statistics containers, which can always
         minimazed to save some space on the screen. Most of the charts are interactive, i.e. you can maniupate them to adjsut the scale, to zoom in or zoom out
         and you can always display them in full screen.''')
st.write('''You can perform two kinds of research. Either you can ask for **specific information about journals** related to a field or 
          you can **compare journals** belonging two different fields based on the discriminators that you choose. For instance, you can confront
          cell biology journals and philosophy journals how they tend to mention journals of their own field. Or you can simply
          search for the most mentioned journals in general medicine and see a top 10 of the medical journals in COCI. The fields that you can search for
          are those provided by the All Science Journal Classification (ASJC), which you can always consult [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).
          For istance, if you want to search for medical journals, you might want to search for "General Medicine", instead of just typying "Medicine".
          If you make some mistakes or you submit a field that does not belong to the ASJC codes the system will automatically inform you and suggest you
          possible solutions.''')
st.write('''The application completely run on GitHub thanks to the Streamlit services. The chance of sharing a data science app
         completely for free of course comes with some limits. It is impossible to load the entire COCI dataset and process it in real time
         due to memory limits, thus the whole COCI dataset was pre-processed using the Python Notebook available on the
         [GitHub repository](https://github.com/AleRosae/OpenCitationsCharts) of the application. To conform to the memory limits of Streamlit (1 GB of RAM), only a small 
         portion of the dataset was pre-processed and loaded in the application.''')
st.markdown("""---""")

@st.cache()
def load_data(path):
  with ZipFile(path, 'r') as zip:
    with zip.open('output_2020-04-25T04_48_36_1.json') as infile:
      d = json.load(infile)
      return d
if 'data' not in st.session_state:
  data = load_data(r'output_2020-04-25T04_48_36_1.zip')
  st.session_state['data'] = data
else:
  data = st.session_state['data']

if 'init' not in st.session_state:
  init = parse_initial.initial_parsing(data)
  st.session_state['init'] = init
else:
  init = st.session_state['init']

if 'self_citations_asjc' not in st.session_state:
  d_self_citations_asjc = parse_COCI.self_citation(data, asjc_fields=True)
  st.session_state['self_citations_asjc'] = d_self_citations_asjc
else:
  d_self_citations_asjc = st.session_state['self_citations_asjc']

if 'source_journals' not in st.session_state:
  source_journals = parse_COCI.parse_data(data)
  st.session_state['source_journals'] = source_journals
else:
  source_journals = st.session_state['source_journals']

if 'source_fields' not in st.session_state:
  source_fields = parse_COCI.parse_data(data, asjc_fields=True)
  st.session_state['source_fields'] = source_fields
else:
  source_fields = st.session_state['source_fields']
  
if 'df_distribution' not in st.session_state:
  list_distribution = init['tot_citations_distribution']
  list_distribution = [el for el in list_distribution if el < 100]
  list_outliers = [el for el in list_distribution if el > 100]
  for i in range(len(list_outliers)):
    list_distribution.append(100)
  df_distribution = pd.DataFrame({'d_citations': list_distribution})
  st.session_state['df_distribution'] = df_distribution
else:
  df_distribution = st.session_state['df_distribution']
  
if 'self_citations' not in st.session_state:
  d_self_citations = parse_COCI.self_citation(data)
  st.session_state['self_citations'] = d_self_citations
else:
  d_self_citations = st.session_state['self_citations']

expander_state = True
col7, col8 = st.columns([3, 1])
st.sidebar.header('Simple bibliometric analysis')
st.sidebar.write('Here you can perform simple bibliometric analysis, either by searching for a single academic field or making comparison between two or more fields.')
search_choice = st.sidebar.radio('', ('Single field search', 'Compare different fields'))
if search_choice == 'Single field search':
  st.sidebar.header('Single field search')
  single_search = st.sidebar.radio(
      "What do you want to search for?",
      ('Top journals cited by a field', 'Top journals cited by another journal','Self citations of a field', 'Citations flow'))
  if single_search == 'Top journals cited by a field':
    st.sidebar.write('Use the box below to retrieve journals belonging to a specific field that have received more citations.')
    input_field = st.sidebar.text_input('Journal field', '', key=1234, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                          You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''')
  elif single_search == 'Top journals cited by another journal':
    st.sidebar.write('Use the box below to retrieve journals that receive most citations from a specific journal (except itself!).')
    input_field = st.sidebar.text_input('Journal name', '', key=12335464, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                          You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''')
  elif single_search == 'Self citations of a field':
    st.sidebar.write('''Use the box below to search for a specific field and see how it tends to mention works belonging to the same fields''')
    input_field = st.sidebar.text_input('Journal field', '', key=123, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                              You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''')
  elif single_search == 'Citations flow':
    st.sidebar.write('''Use the box below to search for a specific field and see which are the other fields (itself excluded) that receive 
        more citations from it.''')
    input_field = st.sidebar.text_input('Journal field', '', key=1122, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                              You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''')
  button = st.sidebar.button('Go', key= 91239)
  if button and input_field != '' and single_search == 'Top journals cited by a field':
    result_mistakes = parse_COCI.spelling_mistakes(input_field)
    if result_mistakes == False:
      result = parse_COCI.parse_data(data, asjc_fields = True, specific_field=input_field)
      with col8:
        st.markdown('***')
        st.write(f'''There are **{str(len(result[input_field].keys()))} journals** related to **{input_field}**, for a total of **{str(sum(result[input_field].values()))} citations**.
        The most important journal is _{list(result[input_field].keys())[0]}_, which received {list(result[input_field].values())[0]} citations.
        The journal with less citations is _{list(result[input_field].keys())[-1]}_, which was mentioned only {list(result[input_field].values())[-1]} times.''')
        if sum(list(result[input_field].values())) > round(np.mean(list(source_fields['fields'].values()))):
          st.write(f'''Overall, there is **total of {sum(list(result[input_field].values()))} mentions** related to the field of **{input_field}**.
                    This is higher then the average number of citations for a single field ({round(np.mean(list(source_fields['fields'].values())))}).''')   
        else:
          st.write(f'''Overall, there is **total of {sum(list(result[input_field].values()))} mentions** related to the field of **{input_field}**.
                  This is below the average number of citations for a single field ({round(np.mean(list(source_fields['fields'].values())))}).''')  
        st.write(f'''The average number of citations for each journal of {input_field} is around {round(mean(result[input_field].values()))}.''') 
      with col7:
        st.header(f'The most cited journals of {input_field}')
        source = pd.DataFrame({'journals': list(result[input_field].keys())[:10], 'values': list(result[input_field].values())[:10]})
        bars = alt.Chart(source).mark_bar(size=30, align="center", binSpacing=1).encode(
            y=alt.Y('journals', sort='-x'),
            x=alt.X('values', title='Number of citations'),
            color=alt.Color('values',  scale=alt.Scale(scheme='purples'))
        ).properties(height=800)
        st.altair_chart(bars.interactive(), use_container_width=True)
      st.markdown('***')
    elif result_mistakes == None:
      st.sidebar.write(f"Can't find {input_field}. Check the spelling")
    else:
      result_mistakes = str(result_mistakes[input_field]).strip('][')
      st.sidebar.write(f"Can't find {input_field}. Did you mean one of the following: {result_mistakes} ?")
      
  elif button and input_field != "" and single_search == 'Top journals cited by another journal':
    result_mistakes = parse_COCI.spelling_mistakes(input_field, journal=True)
    if result_mistakes == False:
      result = parse_COCI.search_specific_journal(data,specific_journal=input_field)
      with col8:
        st.markdown('***')
      with col7:
        st.header(f'The journals that are cited the most by {input_field}')
        source = pd.DataFrame({'journals': list(result.keys())[:10], 'values': list(result.values())[:10]})
        bars = alt.Chart(source).mark_bar(size=30, align="center", binSpacing=1).encode(
            y=alt.Y('journals', sort='-x'),
            x=alt.X('values', title='Number of citations'),
            color=alt.Color('values',  scale=alt.Scale(scheme='purples'))
        ).properties(height=800)
        st.altair_chart(bars.interactive(), use_container_width=True)
      st.markdown('***')
    elif result_mistakes == None:
      st.sidebar.write(f"Can't find {input_field}. Check the spelling")
    else:
      result_mistakes = str(result_mistakes[input_field]).strip('][')
      st.sidebar.write(f"Can't find {input_field}. Did you mean one of the following: {result_mistakes} ?")
    
  elif button and input_field != "" and single_search == 'Self citations of a field':
    check_spelling_selfcit = parse_COCI.spelling_mistakes(input_field)
    if check_spelling_selfcit == False:
      self_citation_field = parse_COCI.self_citation(data, asjc_fields=True, specific_field=input_field)
      df_selfcit = pd.DataFrame({'category': self_citation_field.keys(), 'value': self_citation_field.values()})
      with col7:
        st.header(f'Self citations of {input_field}')
        st.altair_chart(alt.Chart(df_selfcit).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative", sort=list(self_citation_field.keys())),
            color=alt.Color(field="category", type="nominal", sort=list(self_citation_field.keys()))), use_container_width=True)
      with col8:
        global_percentages = [re.search(r"\(.*\)", el).group().strip(')(') for el in d_self_citations_asjc.keys()]
        st.markdown('***')
        st.write(f'''The pie chart displays how many articles related to **{input_field}** tend to mention
                  articles related to the same field. It is a rough discriminator of how a field tend to cross its disciplinary boundaries
                  and cross with external subjects. Self citations are scored when an article mention another article belonging to
                  the same exact ASJC code, while partial self citations includes articles that are not the exact match but
                  that belong to the same ASJC group.''')
        st.write(f'''In **{input_field}** there are **{df_selfcit.iloc[0,1]} self citations** (global percentage is {global_percentages[0]}),
        **{df_selfcit.iloc[1,1]} partial self-citations** (global percentage is {global_percentages[1]})
        and **{df_selfcit.iloc[2,1]} not self citations** (global percentage is {global_percentages[2]}).''')
      st.markdown('***')
    elif check_spelling_selfcit == None:
      st.sidebar.write(f"Can't find {input_field}. Check the spelling.")
    else:
      check_spelling_selfcit = str(check_spelling_selfcit[input_field]).strip('][')
      st.sidebar.write(f"Can't find {input_field}. Did you mean one of the following: {check_spelling_selfcit} ?")

  elif button and  input_field != '' and single_search == 'Citations flow':
    col7, col8 = st.columns([2, 1])
    check_spelling_selfcit = parse_COCI.spelling_mistakes(input_field)
    if check_spelling_selfcit == False:
      source_citflow = parse_COCI.citations_flow(data, specific_field=input_field)
      df_citflow = pd.DataFrame({'fields': list(source_citflow['fields'].keys())[:10], 'values': list(source_citflow['fields'].values())[:10]})
      with col7:
        st.header(f'Citations flow in {input_field}')
        bars = alt.Chart(df_citflow).mark_bar(size=30, align="center", binSpacing=1).encode(
            y=alt.Y('fields', sort='-x'),
            x='values',
            color=alt.Color('values')
        ).properties(height=800)
        st.altair_chart(bars.interactive(), use_container_width=True)
      with col8:
        tot_cit_supergroups = sum(source_citflow['supergroups'].values())
        cit_supergroups_categories = [el + ' (' + str(round((source_citflow['supergroups'][el]/tot_cit_supergroups) * 100))+'%)' for el in source_citflow['supergroups'].keys()]
        df_cit_source_supergroups = pd.DataFrame({'category': cit_supergroups_categories, 
                                        'values': source_citflow['supergroups'].values()})
        st.header(f'''Groups and supergroups subdivision''')
        st.altair_chart(alt.Chart(df_cit_source_supergroups).mark_arc().encode(
          theta=alt.Theta(field="values", type="quantitative", sort=cit_supergroups_categories),
          color=alt.Color(field="category", type="nominal", sort=cit_supergroups_categories)), use_container_width=True)
        
        #voglio solo i primi 10 categorie/valori, il resto va nella categoria others
        tot_cit_groups = sum(source_citflow['groups'].values())
        cit_groups_categories = [el + ' (' + str(round((source_citflow['groups'][el]/tot_cit_groups) * 100))+'%)' for el in source_citflow['groups'].keys()][:10]
        cit_groups_values = list(source_citflow['groups'].values())[:10]
        cit_groups_others = sum(list(source_citflow['groups'].values())[10:])
        cit_groups_categories.append('others (' + str(round((cit_groups_others/tot_cit_groups) * 100))+'%)')
        cit_groups_values.append(cit_groups_others)
        df_cit_source_groups = pd.DataFrame({'category': cit_groups_categories, 
                                        'values': cit_groups_values})
        st.altair_chart(alt.Chart(df_cit_source_groups).mark_arc().encode(
          theta=alt.Theta(field="values", type="quantitative", sort=cit_groups_categories),
          color=alt.Color(field="category", type="nominal", sort=cit_groups_categories, scale=alt.Scale(scheme='category20'))), use_container_width=True)
      not_mentioned = str(parse_COCI.check_unmentioned(source_citflow['groups'])).strip('][')
      st.write(f'''The charts above display **how citations have flowed** starting from journals related to **{input_field}**.''')
      st.write(f'''The bar charts illustrates which are the other fields that are mostly citited by articles of **{input_field}**. This 
                provides an idea of how these disciplines tend to communicate. In this case, the **most mentioned field is {list(source_citflow['fields'].keys())[0]}**,
                with **{list(source_citflow['fields'].values())[0]} citations**. The **least one is {list(source_citflow['fields'].keys())[-1]}**, which apparentely is the most distant
                subject from {input_field}, with **only {list(source_citflow['fields'].values())[-1]} mentions**.''')
      st.write('''The pie charts on the right column illustrate the same information but according to the **groups/supergroups**
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
      
elif search_choice == 'Compare different fields':
  st.sidebar.header('Compare different fields')
  multiple_search = st.sidebar.radio(
      "What do you want to search for?",
      ('Number of citations', 'Self citations', 'Citations flow', 'Journals flow'))
  if multiple_search == 'Number of citations':
    st.sidebar.write('Use the box below to make comparison between the number of citations received for different academic fields. Simply type a list of fields to compare.')
    input_compare_field = st.sidebar.text_area('Fields (separated with comma and space)', '', key=4321, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                              You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''')
    input_compare_field_cited = None
    button = st.sidebar.button('Go', key=7777)
  elif multiple_search == 'Self citations':
    st.sidebar.write('''Use the box below to make comparison of how much two fields tend to mention themselves.''')
    input_compare_field = st.sidebar.text_input('Field 1', '', key=3342, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                              You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''')
    input_compare_field_cited = st.sidebar.text_input('Field 2', '', key=234235, help='''Fields must corrispond to ASJC fields (case insensitive). ''')
    button = st.sidebar.button('Go', key=8888)  
  elif multiple_search == 'Citations flow':
    st.sidebar.write('''Use the box below to confront the citations flow (i.e. where a specific fields citations go to)
                    of two different fields.''')
    input_compare_field= st.sidebar.text_input('Field 1', '', key=11223433, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                              You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''')
    input_compare_field_cited = st.sidebar.text_input('Field 2', '', key=234235, help='''Fields must corrispond to ASJC fields (case insensitive). ''')
    button = st.sidebar.button('Go', key = 9988)

  elif multiple_search == 'Journals flow':
    st.sidebar.write('''Use the box below to look at which journals of a specific field receive more citations from journals
    of another field. You might be particularly interested in fields fairly distant (e.g. philosophy and general medicine).''')
    input_compare_field= st.sidebar.text_input('Field that has cited', '', key=12456, help='''Fields must corrispond to ASJC fields (case insensitive). 
                                              You can check the full list [here](https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications).''')
    input_compare_field_cited = st.sidebar.text_input('Journals of a field that received citations', '', key=12312, help='''Fields must corrispond to ASJC fields (case insensitive). ''')
    button = st.sidebar.button('Go', key=9999)

  if input_compare_field != '' and multiple_search == 'Number of citations' and button: 
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
      result = parse_COCI.parse_data(data, asjc_fields=True)['fields']
      output = {}
      result = {k.lower():v for k, v in result.items()}
      for item in input:
        output[item.capitalize()] = result[item.lower()]
    if render == True:
      source = pd.DataFrame({'fields': output.keys(), 'values': output.values()})
      bars = alt.Chart(source).mark_bar(size=40, align="center", binSpacing=1).encode(
        y=alt.Y('fields', sort='-x'),
        x=alt.X('values', title='Number of citations'),
        color=alt.Color('values')
        ).properties(height=800)
      st.header('Citations comparison by different fields')
      st.altair_chart(bars.interactive(), use_container_width=True)
      st.markdown('***')

  elif input_compare_field != '' and input_compare_field_cited != '' and multiple_search == 'Self citations' and button: 
    col7, col8 = st.columns(2)
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
      self_citation_field_1 = parse_COCI.self_citation(data, asjc_fields=True, specific_field=input[0])
      df_selfcit_1 = pd.DataFrame({'category': self_citation_field_1.keys(), 'value': self_citation_field_1.values()})
      self_citation_field_2 = parse_COCI.self_citation(data, asjc_fields=True, specific_field=input[1])
      df_selfcit_2 = pd.DataFrame({'category': self_citation_field_2.keys(), 'value': self_citation_field_2.values()})
      st.write(f'''These pie charts **confront* how many articles** related to **{input_compare_field}** and **{input_compare_field_cited}** tend to mention
                  articles related to the **same field**. It is a rough discriminator of **how much a field tend to cross its disciplinary boundaries**
                  and cross with external subjects. Self citations are scored when an article mention another article belonging to
                  the same exact ASJC code, while partial self citations includes articles that are not the exact match but
                  that belong to the same ASJC group.''')
      global_percentages = [re.search(r"\(.*\)", el).group().strip(')(') for el in d_self_citations_asjc.keys()]
      with col7:
        st.header(f'Self citations of {input[0]}')
        st.write(f'''How many articles belonging to **{input_compare_field}** tend to mention
                  articles related to the same field.''')
        st.altair_chart(alt.Chart(df_selfcit_1).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative", sort=list(self_citation_field_1.keys())),
            color=alt.Color(field="category", type="nominal", sort=list(self_citation_field_1.keys()))), use_container_width=True)
        st.write(f'''In **{input_compare_field}** there are **{df_selfcit_1.iloc[0,1]} self citations** (global percentage is {global_percentages[0]}),
        **{df_selfcit_1.iloc[1,1]} partial self-citations** (global percentage is {global_percentages[1]})
        and **{df_selfcit_1.iloc[2,1]} not self citations** (global percentage is {global_percentages[2]}).''')
      with col8:
        st.header(f'Self citations of {input[1]}')
        st.write(f'''How many articles belonging to **{input_compare_field_cited}** tend to mention
                  articles related to the same field.''')
        st.altair_chart(alt.Chart(df_selfcit_2).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative", sort=list(self_citation_field_2.keys())),
            color=alt.Color(field="category", type="nominal", sort=list(self_citation_field_2.keys()))), use_container_width=True)
        st.write(f'''In **{input_compare_field_cited}** there are **{df_selfcit_2.iloc[0,1]} self citations** (global percentage is {global_percentages[0]}),
        **{df_selfcit_2.iloc[1,1]} partial self-citations** (global percentage is {global_percentages[1]})
        and **{df_selfcit_2.iloc[2,1]} not self citations** (global percentage is {global_percentages[2]}).''')
    st.markdown('***')
  elif input_compare_field != '' and input_compare_field_cited != '' and multiple_search == 'Citations flow' and button: 
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
      col7, col8 = st.columns(2)
      source_citflow_1 = parse_COCI.citations_flow(data, specific_field=input[0])
      source_citflow_2 = parse_COCI.citations_flow(data, specific_field=input[1])
      df_citflow_1 = pd.DataFrame({'fields': list(source_citflow_1['fields'].keys())[:10], 'values': list(source_citflow_1['fields'].values())[:10]})
      df_citflow_2 = pd.DataFrame({'fields': list(source_citflow_2['fields'].keys())[:10], 'values': list(source_citflow_2['fields'].values())[:10]})
      with col7:
        st.header(f'Citations flow in {input[0]}')
        bars = alt.Chart(df_citflow_1).mark_bar(size=30, align="center", binSpacing=1).encode(
            y=alt.Y('fields', sort='-x'),
            x=alt.X('values', title='Number of citations'),
            color=alt.Color('values')
        ).properties(height=800)
        st.altair_chart(bars.interactive(), use_container_width=True)
        tot_cit_supergroups_1 = sum(source_citflow_1['supergroups'].values())
        cit_supergroups_categories_1 = [el + ' (' + str(round((source_citflow_1['supergroups'][el]/tot_cit_supergroups_1) * 100))+'%)' for el in source_citflow_1['supergroups'].keys()]
        df_cit_source_supergroups_1 = pd.DataFrame({'category': cit_supergroups_categories_1, 
                                        'values': source_citflow_1['supergroups'].values()})
        st.header(f'''Groups and supergroups subdivision''')
        st.altair_chart(alt.Chart(df_cit_source_supergroups_1).mark_arc().encode(
          theta=alt.Theta(field="values", type="quantitative"),
          color=alt.Color(field="category", type="nominal")), use_container_width=True)
        #voglio solo i primi 10 categorie/valori, il resto va nella categoria others
        tot_cit_groups_1 = sum(source_citflow_1['groups'].values())
        cit_groups_categories_1 = [el + ' (' + str(round((source_citflow_1['groups'][el]/tot_cit_groups_1) * 100))+'%)' for el in source_citflow_1['groups'].keys()][:10]
        cit_groups_values_1 = list(source_citflow_1['groups'].values())[:10]
        cit_groups_others_1 = sum(list(source_citflow_1['groups'].values())[10:])
        cit_groups_categories_1.append('other (' + str(round((cit_groups_others_1/tot_cit_groups_1) * 100))+'%)')
        cit_groups_values_1.append(cit_groups_others_1)
        df_cit_source_groups_1 = pd.DataFrame({'category': cit_groups_categories_1, 
                                        'values': cit_groups_values_1})
        st.altair_chart(alt.Chart(df_cit_source_groups_1).mark_arc().encode(
          theta=alt.Theta(field="values", type="quantitative", sort=cit_groups_categories_1),
          color=alt.Color(field="category", type="nominal", sort=cit_groups_categories_1)), use_container_width=True)
      with col8:
        st.header(f'Citations flow in {input[1]}')
        bars = alt.Chart(df_citflow_2).mark_bar(size=30, align="center", binSpacing=1).encode(
            y=alt.Y('fields', sort='-x'),
            x=alt.X('values', title='Number of citations'),
            color=alt.Color('values')
        ).properties(height=800)
        st.altair_chart(bars.interactive(), use_container_width=True)
        tot_cit_supergroups_2 = sum(source_citflow_2['supergroups'].values())
        cit_supergroups_categories_2 = [el + ' (' + str(round((source_citflow_2['supergroups'][el]/tot_cit_supergroups_2) * 100))+'%)' for el in source_citflow_2['supergroups'].keys()]
        df_cit_source_supergroups_2 = pd.DataFrame({'category': cit_supergroups_categories_2, 
                                        'values': source_citflow_2['supergroups'].values()})
        st.header(f'''Groups and supergroups subdivision''')
        st.altair_chart(alt.Chart(df_cit_source_supergroups_2).mark_arc().encode(
          theta=alt.Theta(field="values", type="quantitative"),
          color=alt.Color(field="category", type="nominal")), use_container_width=True)
        #voglio solo i primi 10 categorie/valori, il resto va nella categoria others
        tot_cit_groups_2 = sum(source_citflow_2['groups'].values())
        cit_groups_categories_2 = [el + ' (' + str(round((source_citflow_2['groups'][el]/tot_cit_groups_2) * 100))+'%)' for el in source_citflow_2['groups'].keys()][:10]
        cit_groups_values_2 = list(source_citflow_2['groups'].values())[:10]
        cit_groups_others_2 = sum(list(source_citflow_2['groups'].values())[10:])
        cit_groups_categories_2.append('other (' + str(round((cit_groups_others_2/tot_cit_groups_2) * 100))+'%)')
        cit_groups_values_2.append(cit_groups_others_2)
        df_cit_source_groups_2 = pd.DataFrame({'category': cit_groups_categories_2, 
                                        'values': cit_groups_values_2})
        st.altair_chart(alt.Chart(df_cit_source_groups_2).mark_arc().encode(
          theta=alt.Theta(field="values", type="quantitative", sort=cit_groups_categories_2),
          color=alt.Color(field="category", type="nominal", sort= cit_groups_categories_2)), use_container_width=True)
    st.markdown('***')
  elif button and multiple_search == 'Journals flow' and input_compare_field != '' and input_compare_field_cited != '': 
    col7, col8 = st.columns([4, 1])
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
      source_citflow_journal = parse_COCI.citations_flow_journals(data, specific_fields=input)
      df_source_citflow_journal = pd.DataFrame({'fields': list(source_citflow_journal.keys())[:10], 'values': list(source_citflow_journal.values())[:10]})
      with col7:
        st.header(f'Journals citations flow')
        bars = alt.Chart(df_source_citflow_journal).mark_bar(size=30, align="center", binSpacing=1).encode(
            y=alt.Y('fields', sort='-x'),
            x='values',
            color=alt.Color('values', scale=alt.Scale(scheme='purples'))
        ).properties(height=800)
        st.altair_chart(bars.interactive(), use_container_width=True)
      with col8:
        st.markdown("***")
        st.write(f'''The bar chart on the left display the **main journals** related to **{input_compare_field_cited}** that have been
              ** mentioned by** journals of **{input_compare_field}**.''')
        st.write(f'''The **most popular journal of {input_compare_field_cited}** among researchers of **{input_compare_field}** is 
                    _{list(source_citflow_journal.keys())[0]}_, with **{list(source_citflow_journal.values())[0]} mentions**.''')
        st.write(f'''**In total**, there are **{len(list(source_citflow_journal.keys()))} journals of {input_compare_field_cited}** that
                  have been cited by articles related to **{input_compare_field}**. The total number of citations received amount
                  to {sum(list(source_citflow_journal.values()))}.''')
    st.markdown('***')

st.header('General statistics')
st.write('Here you can see various statistics about the whole COCI dataset.')   
if button:
  expander_state = False
with st.expander('General statistics', expanded =expander_state):
  st.write(f'''The **COCI dataset** contains a **total of {sum(init['tot_citations_distribution'])} citations**, which are
            distributed in **{str(init['journals'])} unique journals**, which cover **exactly {len(source_fields['fields'].keys())} different academic fields** and that can be
            grouped in **{len(source_fields['groups'].keys())} different groups** according to the _All Science Journals Classification_ (**ASJC**).
            Here you can see which are the most important journals in the dataset and which are the fields most covered by them.''')
  col5, col6 = st.columns(2)
  with col5:
    st.header('Most important journals')
    df_source_journals = pd.DataFrame({'journals': list(source_journals.keys())[:10], 'values': list(source_journals.values())[:10]}) #prendo solo i primi 10
    bars = alt.Chart(df_source_journals).mark_bar(size=20, align="center", binSpacing=1).encode(
        y=alt.Y('journals', sort='-x'),
        x=alt.X('values', title='Number of citations'),
        color=alt.Color('values',  scale=alt.Scale(scheme='purples'))
    ).properties(height=600)
    st.altair_chart(bars.interactive(), use_container_width=True)
    st.write(f'''The chart displays the **journals that received the most number of citations**. The **most cited journal** is _{list(source_journals.keys())[0]}_,
             with the astonishing number of **{list(source_journals.values())[0]} citations**. The **least cited journal** is _{list(source_journals.keys())[-1]}_,
             which received only {list(source_journals.values())[-1]} mentions.''')
  with col6:
    st.header('''Most popular academic fields''')
    df_source_fields = pd.DataFrame({'fields': list(source_fields['fields'].keys())[:10], 'values': list(source_fields['fields'].values())[:10]})
    bars = alt.Chart(df_source_fields).mark_bar(size=20, align="center", binSpacing=0.5).encode(
        y=alt.Y('fields', sort='-x'),
        x=alt.X('values', title='Number of citations'),
        color=alt.Color('values')
    ).properties(height=600)
    st.altair_chart(bars.interactive(), use_container_width=True)
    st.write(f'''The chart displays the **fields that received the most number of citations**. The **most popular field** is **{list(source_fields['fields'].keys())[0]}**,
             with the astonishing number of **{list(source_fields['fields'].values())[0]} citations**. The least popular one is **{list(source_fields['fields'].keys())[-1]}**,
             which received only {list(source_fields['fields'].values())[-1]} mentions.''')
  col3, col4 = st.columns(2)
  with col3:
    st.header(f"Distribution of citations")
    base = alt.Chart(df_distribution)
    bar = base.mark_bar().encode(
        x=alt.X('d_citations:Q', bin = alt.BinParams(nice=True, maxbins=100), title='Number of citations'),
        y=alt.Y('count()', title = 'Number of istances')
    )
    st.altair_chart(bar.interactive(), use_container_width=True)
    st.write(f'''**Distribution of the number of citations** for each citing article. _NB: all the values above 100 were approximated as 100 due to the fact
            that the original data were particularly skewed (most of the values ended up being near 1)._''')
    st.write(f'''The **average number of citations** for citing articles is **{init['average_citations']}**, the mode is **{mode(init['tot_citations_distribution'])}**.
            The **maximum value** is **{max(init['tot_citations_distribution'])}**, while the **minimum is {min(init['tot_citations_distribution'])}**.''')
  with col4:
    st.header('Unique journals')
    tot_set = init['citing_set'] + init['cited_set'] + init['cited_also_citing']
    df_unique_journals = pd.DataFrame({'category': ['Only citing ('+str(round((init['citing_set']/tot_set) * 100))+'%)', 
                                                    'Only cited ('+str(round((init['cited_set']/tot_set) * 100))+'%)'
                                                    , 'cited also citing ('+str(round((init['cited_also_citing']/tot_set) * 100))+'%)'], 
                                      'value': [init['citing_set'], init['cited_set'], init['cited_also_citing']]})
    st.altair_chart(alt.Chart(df_unique_journals).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="category", type="nominal")), use_container_width=True)
    st.write('''Whether each **unique journal** appears only as a citing article (and do not receive citation), as a cited article (and do not cite other articles)
            or both (articles that both cite other articles and receive citations).''')

with st.expander('Fields subdivision', expanded=expander_state):
  st.write('''The bar chart above displays the **most important fields**. However, **ASJC** also comes with a subdivion of those fields in
           more general groups that give us a general picture of the subjects that are covered. These charts offer a broader look at the composition
           of the COCI dataset by illustrating **the groups** in which each field falls and their **relative supergroups** (i.e. the most general
           subdivision possible).''')
  st.header('''All the academic groups''')
  df_source_groups = pd.DataFrame({'groups': list(source_fields['groups'].keys()), 'values': list(source_fields['groups'].values())})
  bars = alt.Chart(df_source_groups).mark_bar(size=20, align="center", binSpacing=0.5).encode(
      y=alt.Y('groups', sort='-x'),
      x='values',
      color=alt.Color('values',scale=alt.Scale(scheme='tealblues') )
  ).properties(height=600)
  st.altair_chart(bars.interactive(), use_container_width=True)
  col9, col10 = st.columns(2)
  with col9:
    st.header('''Academic groups subdivision''')
    tot_groups = sum(source_fields['groups'].values())
    groups_categories = [el + ' (' + str(round((source_fields['groups'][el]/tot_groups) * 100))+'%)' for el in source_fields['groups'].keys()][:15]
    groups_values = list(source_fields['groups'].values())[:15]
    groups_others = sum(list(source_fields['groups'].values())[15:])
    groups_categories.append('others (' + str(round((groups_others/tot_groups) * 100))+'%)')
    groups_values.append(groups_others)
    df_source_groups = pd.DataFrame({'category': groups_categories, 
                                    'values': groups_values})
    st.altair_chart(alt.Chart(df_source_groups).mark_arc().encode(
      theta=alt.Theta(field="values", type="quantitative", sort=groups_categories),
      color=alt.Color(field="category", type="nominal", sort=groups_values, scale=alt.Scale(scheme='category20'))), use_container_width=True) #add colour scheme for more colours in the pie chart
      
    st.write(f'''The **subdivision** of the {len(source_fields['fields'].keys())} fields present in the COCI dataset in **groups**. The **most popular group**
            is **{list(source_fields['groups'].keys())[0]}** which received **{list(source_fields['groups'].values())[0]} mentions**. The least popular one is 
             {list(source_fields['groups'].keys())[-1]} with {list(source_fields['groups'].values())[-1]} citations. 
             _Others_ include: {str(list(source_fields['groups'].keys())[15:]).strip('][')}.''')
    with col10:
      st.header('''Academic supergroups subdivision''')
      tot_supergroups = sum(source_fields['supergroups'].values())
      supergroups_categories = [el + ' (' + str(round((source_fields['supergroups'][el]/tot_supergroups) * 100))+'%)' for el in source_fields['supergroups'].keys()]
      df_source_supergroups = pd.DataFrame({'category': supergroups_categories, 
                                      'value': source_fields['supergroups'].values()})
      st.altair_chart(alt.Chart(df_source_supergroups).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative", sort=supergroups_categories),
        color=alt.Color(field="category", type="nominal", sort=supergroups_categories)), use_container_width=True)
      st.write(f'''The **subdivision** of the {len(source_fields['groups'].keys())} groups present in the COCI dataset according to supergroups. The** most popular supergroup** is
             **{list(source_fields['supergroups'].keys())[0]}** which received **{list(source_fields['supergroups'].values())[0]} mentions**. The least popular one is 
             {list(source_fields['supergroups'].keys())[-1]} with {list(source_fields['supergroups'].values())[-1]} citations.''')
  
with st.expander("Citations flow", expanded=expander_state):
  st.write('''How does citations flow between different journals or fields? In this section you can see whether articles belonging to a specific field or journal
          **tend to mention publications that belong to the same field or journal**. This is particularly interesting because it give us an idea of how much the journals in the dataset are
          **cross-disciplinary**. With the sidebar you can also see statistics related to one specific field in order to see which are the subject that are more 
           prone to cross the boundaries between different fields. ''')
  col1, col2 = st.columns(2)
  with col2:
    st.header('Self citations (by journals)')
    df_d = pd.DataFrame({'category': d_self_citations.keys(), 'value': d_self_citations.values()})
    st.altair_chart(alt.Chart(df_d).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="category", type="nominal"))  , use_container_width=True)
    st.write('Articles that mention publications that belong to the same journal of the citing article.')
  with col1:
    st.header('Self citations (by academic field)')
    df_d = pd.DataFrame({'category': d_self_citations_asjc.keys(), 'value': d_self_citations_asjc.values()})
    st.altair_chart(alt.Chart(df_d).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative", sort=list(d_self_citations.keys())),
        color=alt.Color(field="category", type="nominal", sort=list(d_self_citations.keys()))), use_container_width=True)
    st.write('Articles that mention publications belonging to the same academic field or of similar academic field (according to ASJC classification).')
