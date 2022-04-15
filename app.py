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
  'About': 'Alessandro Rosa, DHARC - Unviersity of Bologna.'})
st.title('''OpenCitations in Charts''')
st.write('### A web application for visualizing the articles in the COCI dataset.')
st.write('Start exploring COCI using the left sidebar! Choose your type of query, ask for a specific field or journal, and see the results!')
st.markdown('***')

@st.cache()
def load_csvs():
  csvs = parse_COCI.load_csvs()
  return csvs

@st.cache()
def load_data():
  with open(r"results/journals_cited_by_field_results.json", 'r') as fp:
    single_field_data = json.load(fp)
  with open(r'results/journals_cited_by_journal_results.json', 'r') as fp:
    single_journals_data = json.load(fp)
  with open(r'results/self_citations_by_field_results.json', 'r') as fp:
    self_citations_data = json.load(fp)
  with open(r'results/citations_flow_by_field_results.json', 'r') as fp:
    citations_flow_data = json.load(fp)
  with open(r'results/cross_citations_flow_by_field_results.json', 'r') as fp:
    cross_citations_flow_data = json.load(fp)
  
  data = {"single_field_data": single_field_data, "single_journals_data" : single_journals_data, 
          "self_citations_data": self_citations_data, "citations_flow_data": citations_flow_data, 
          "cross_citations_flow_data": cross_citations_flow_data}

  return data

if 'data' not in st.session_state:
  data = load_data()
  st.session_state['data'] = data
else:
  data = st.session_state['data']

if 'csvs' not in st.session_state:
  csvs = load_csvs()
  st.session_state['csvs'] = csvs
else:
  csvs = st.session_state['csvs']


col7, col8 = st.columns([3, 1])

st.sidebar.write('''Choose between one single input query or multiple inputs analysis, fill the text boxes
                  and then **press Go**.''')
search_choice = st.sidebar.radio('', ('Single field', 'Multiple fields'))
if search_choice == 'Single field':
  single_search = st.sidebar.selectbox(
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
      input_field = input_field.lower()
      result = data['single_field_data'][input_field]
      with col8:
        st.markdown('***')
        if sum(list(result[input_field].values())) > 10: #placeholder per la media di citazioni globali
          st.write(f'''In the COCI dataset there are **{str(len(result[input_field].keys()))} journals** related to **{input_field}**,
            for a total of **{str(sum(result[input_field].values()))} citations**.
          This is higher than the average number of citations for a single field (10).''')
        else:
          st.write(f'''There are **{str(len(result[input_field].keys()))} journals** related to **{input_field}**, for a total of **{str(sum(result[input_field].values()))} citations**.
          This is below the average number of citations for a single field (10).''')
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

    elif result_mistakes == None:
      st.sidebar.write(f"Can't find {input_field}. Check the spelling")
    else:
      result_mistakes = str(result_mistakes[input_field]).strip('][')
      st.sidebar.write(f"Can't find {input_field}. Did you mean one of the following: {result_mistakes} ?")
      
  elif button and input_field != "" and single_search == 'Top journals cited by another journal':
    result_mistakes = parse_COCI.spelling_mistakes(input_field, journal=True)
    if result_mistakes == False:
      input_field = input_field.lower()
      result = data['single_journals_data'][input_field]
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


    elif result_mistakes == None:
      st.sidebar.write(f"Can't find {input_field}. Check the spelling")
    else:
      result_mistakes = str(result_mistakes[input_field]).strip('][')
      st.sidebar.write(f"Can't find {input_field}. Did you mean one of the following: {result_mistakes} ?")
    
  elif button and input_field != "" and single_search == 'Self citations of a field':
    check_spelling_selfcit = parse_COCI.spelling_mistakes(input_field)
    if check_spelling_selfcit == False:
      self_citation_field = data['self_citations_data'][input_field.lower()]
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
      st.write(f'''The charts below display **how citations have flowed** starting from journals related to **{input_field}**. It is a general overview of how different
                  academic fields interact with each other, using citations as a proxy for linking two different fields.''')
      col7, col8 = st.columns(2)
      input_field = input_field.lower()
      source_citflow = data['citations_flow_data'][input_field]
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

      st.write(f'''The bar chart illustrates which are the other fields that are mostly cited by articles of **{input_field}**. This 
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
  multiple_search = st.sidebar.selectbox(
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
    st.sidebar.write('''Display a comparison between **exactly two fields** in terms of how much they tend to mention disciplines belonging to their own field.''')
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
      st.sidebar.write(f'''Can't find {input[index_cantfind]}. Check the spelling. Remember that you have to separate the fields only
                        with a comma and space, do not press enter!''')
      render = False
    elif len(dict_spelling)> 0:
      for dic in dict_spelling:
        for input_key, mistake_value in dic.items():
          mistake_value = str(mistake_value).strip('][')
          st.sidebar.write(f"Can't find {input_key}. Did you mean one of the following: {mistake_value} ?")
          render = False    
    else: 
      result = data['citations_flow_data']
      output = {}
      for item in input:
        output[item] = sum(result[item.lower()]["fields"].values())
        print(output)
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
      self_citation_field_1 = data['self_citations_data'][input[0].lower()]
      df_selfcit_1 = pd.DataFrame({'fields': self_citation_field_1.keys(), 'values': self_citation_field_1.values()})
      self_citation_field_2 = data['self_citations_data'][input[1].lower()]
      df_selfcit_2 = pd.DataFrame({'fields': self_citation_field_2.keys(), 'values': self_citation_field_2.values()})
      st.header('Self citations comparison')
      st.write(f'''These pie charts **confront how many articles** related to **{input_compare_field}** or to **{input_compare_field_cited}** tend to mention
                  articles related to the **same field**. It is a rough discriminator of **how much a field tend to cross its disciplinary boundaries**
                  and cross with external subjects. Self citations are scored when an article mentions another article belonging to
                  the same exact ASJC code, while partial self citations includes articles that are not the exact match but
                  that belong to the same ASJC group. The comparison allows to detect substantial differences in the way in which fields belonging to different groups (e.g. medical sciences
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
      source_citflow_1 = data['citations_flow_data'][input[0].lower()]
      source_citflow_2 = data['citations_flow_data'][input[0].lower()]
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
          'text': f'<b>Groups mentioned both by {input[0]} and {input[1]}',
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
      input = str((input[0].lower(), input[1].lower()))
      print(input)
      source_citflow_journal = data['cross_citations_flow_data'][input]
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
                Here you can see some information about it, provided that 
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