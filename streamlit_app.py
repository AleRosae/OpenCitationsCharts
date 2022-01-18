from altair.vegalite.v4.schema.core import Align
from pandas.core.algorithms import mode
import streamlit as st
import re
import json
import pandas as pd
from streamlit.type_util import Key
import parse_COCI
import parse_initial
import altair as alt
import scipy.stats as stats
from statistics import mode
from zipfile import ZipFile

st.set_page_config(page_title='OpenCitationsCharts', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.write('''
         # Demo
         ### This is a premimilary version of the OpenCitations web platform for visualizing statistics.
         The first time you open the app it takes some time to load the entire dataset, don't worry.
         ''')
st.write('''By default the main page loads some statistics about the whole OpenCitations dataset.
         You can use the sidebar to visualize more specific information, either using journals or academic fields
         as discriminators. The charts you ask for appear below the global statistics container. You can minimize this container whenever you want by clicking on the small dash
         here on the right.''')
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

if 'header' not in st.session_state:
  header = (f"There are {str(init['journals'])} unique journals in the COCI dataset and a total of {sum(init['tot_citations_distribution'])} citations. ")
  st.session_state['header'] = header
else:
  header = st.session_state['header']

if 'self_citations_asjc' not in st.session_state:
  d_self_citations_asjc = parse_COCI.self_citation(data, asjc_fields=True)
  st.session_state['self_citations_asjc'] = d_self_citations_asjc
else:
  d_self_citations_asjc = st.session_state['self_citations_asjc']

st.sidebar.header('Retrieve journals of specific fields')
st.sidebar.write('Use the box below to retrieve journals belonging to a specific field that have most citations')
input_journal = st.sidebar.text_input('Journal field', '', help='''Fields must corrispond to ASJC fields (case insensitive). 
                                      You can check the full list here: https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications''')
col7, col8 = st.columns([3, 1])
if input_journal != '':
  result_mistakes = parse_COCI.spelling_mistakes(input_journal)
  if result_mistakes == False:
    result = parse_COCI.parse_data(data)
    with col8:
      st.write(f'''There are {str(len(result.keys()))} journals related to {input_journal} , for a total of {str(sum(result.values()))} citations.
      The most important journal is {list(result.keys())[0]}.''')
    with col7:
      source = pd.DataFrame({'journals': list(result.keys())[:9], 'values': list(result.values())[:9]})
      bars = alt.Chart(source).mark_bar(size=30, align="center", binSpacing=1).encode(
          x=alt.X('journals', sort='-y'),
          y='values'
      ).properties(height=800)
      text = bars.mark_text(
          align='center',
          baseline='middle',
          color = 'white'
      ).encode(
          text='values')
      st.altair_chart(bars+text, use_container_width=True)
  elif result_mistakes == None:
    st.sidebar.write(f"Can't find {input_journal}. Check the spelling")
  else:
    result_mistakes = str(result_mistakes[input_journal]).strip('][')
    st.sidebar.write(f"Can't find {input_journal}. Did you mean one of the following: {result_mistakes} ?")

st.sidebar.header('Compare different fields')
st.sidebar.write('Use the box below to make comparison between the number of citations received for different academic fields. Simply type a list of fields to compare.')
input_compare_field = st.sidebar.text_input('Fields (separated with comma and space)', '', help='''Fields must corrispond to ASJC fields (case insensitive). 
                                            You can check the full list here: https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications''')
if input_compare_field != '': 
  render = True
  input = input_compare_field.split(', ')
  check_spelling = [parse_COCI.spelling_mistakes(inp) for inp in input]
  dict_spelling = [el for el in check_spelling if type(el) == dict]
  if None in check_spelling:
    index_cantfind = check_spelling.index(None)
    st.sidebar.write(f"Can't find {input[index_cantfind]}. Check the spelling")
    render = False
  elif len(dict_spelling)> 0:
    for dic in dict_spelling:
      for input_key, mistake_value in dic.items():
        mistake_value = str(mistake_value).strip('][')
        st.sidebar.write(f"Can't find {input_key}. Did you mean one of the following: {mistake_value} ?")
        render = False    
  else: 
    result = parse_COCI.parse_data(data, asjc_fields=True, n="all")
    output = {}
    result = {k.lower():v for k, v in result.items()}
    for item in input:
      output[item.capitalize()] = result[item.lower()]
  if render == True:
    source = pd.DataFrame({'fields': output.keys(), 'values': output.values()})
    bars = alt.Chart(source).mark_bar(size=40, align="center", binSpacing=1).encode(
      x='fields',
      y='values'
      ).properties(height=800)
    text = bars.mark_text(
      align='center',
      baseline='middle',
      color = 'white'
        ).encode(
        text='values')
    with col7:
      st.altair_chart(bars+text, use_container_width=True)

st.sidebar.header('Self citation by field')
st.sidebar.write('''Use the box below to search for a specific field and see how it tends to mention.
                  works belonging to the same fields''')
input_selfcitation_field = st.sidebar.text_input('Journal field', '', help='''Fields must corrispond to ASJC fields (case insensitive). 
                                            You can check the full list here: https://support.qs.com/hc/en-gb/articles/4406036892562-All-Science-Journal-Classifications''')
if input_selfcitation_field != '':
  check_spelling_selfcit = parse_COCI.spelling_mistakes(input_selfcitation_field)
  if check_spelling_selfcit == False:
    self_citation_field = parse_COCI.self_citation(data, asjc_fields=True, specific_field=input_selfcitation_field)
    df_selfcit = pd.DataFrame({'category': self_citation_field.keys(), 'value': self_citation_field.values()})
    with col7:
      st.header(f'Self citations of {input_selfcitation_field}')
      st.altair_chart(alt.Chart(df_selfcit).mark_arc().encode(
          theta=alt.Theta(field="value", type="quantitative"),
          color=alt.Color(field="category", type="nominal")), use_container_width=True)
      st.write(f'''How many articles belonging to {input_selfcitation_field} tend to mention
                articles related to the same field''')
    with col8:
      global_percentages = [re.search(r"\(.*\)", el).group().strip(')(') for el in d_self_citations_asjc.keys()]
      st.write()
      st.write(f'''In {input_selfcitation_field} there are {df_selfcit.iloc[0,1]} self citations (globa is {global_percentages[0]}),
       {df_selfcit.iloc[1,1]} partial self-citations (global is {global_percentages[1]})
      and {df_selfcit.iloc[2,1]} not self citations (global is {global_percentages[2]}).''')
  elif check_spelling_selfcit == None:
    st.sidebar.write(f"Can't find {input_selfcitation_field}. Check the spelling.")
  else:
    check_spelling_selfcit = str(check_spelling_selfcit[input_selfcitation_field]).strip('][')
    st.sidebar.write(f"Can't find {input_selfcitation_field}. Did you mean one of the following: {check_spelling_selfcit} ?")

with st.expander("Global statistics", expanded=True):
  st.write(header)
  col1, col2 = st.columns(2)
  with col2:
    if 'self_citations' not in st.session_state:
      d_self_citations = parse_COCI.self_citation(data)
      st.session_state['self_citations'] = d_self_citations
    else:
      d_self_citations = st.session_state['self_citations']
    st.header('Self citations (by journals)')
    df_d = pd.DataFrame({'category': d_self_citations.keys(), 'value': d_self_citations.values()})
    st.altair_chart(alt.Chart(df_d).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="category", type="nominal")), use_container_width=True)
    st.write('Articles that cite publications that belong to the same journal of the citing article.')
  with col1:
    st.header('Self citations (by academic field)')
    df_d = pd.DataFrame({'category': d_self_citations_asjc.keys(), 'value': d_self_citations_asjc.values()})
    st.altair_chart(alt.Chart(df_d).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="category", type="nominal")), use_container_width=True)
    st.write('Articles that cite publications of the same academic field or of similar academic field (according to ASJC classification).')

  col3, col4 = st.columns(2)
  with col3:
    if 'df_distribution' not in st.session_state:
      df_distribution = pd.DataFrame({'d_citations': init['tot_citations_distribution']})
      st.session_state['df_distribution'] = df_distribution
    else:
      df_distribution = st.session_state['df_distribution']
    st.header(f"Distribution of citations")
    brush = alt.selection(type='interval')
    points = alt.Chart(df_distribution).mark_point().encode(
      x=alt.X('d_citations:Q', scale = alt.Scale(type='symlog'), title='Citations distribution on a log scale'),
      y=alt.Y('count()',scale = alt.Scale(type='symlog'))).add_selection(brush)
    
    st.altair_chart(points, use_container_width=True)
    st.write(f'''Distribution of the number of citations for each citing article, converted in z-scores and then plotted with a logarithmic scale.
            The average number of citations for citing articles is {init['average_citations']}, the mode is {mode(init['tot_citations_distribution'])}.''')
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
    st.write('''Whether each unique journal appears only as a citing article (and do not receive citation), as a cited article (and do not cite other articles)
            or both (articles that both cite other articles and receive citations)''')
  col5, col6 = st.columns(2)
  with col5:
    if 'source_journals' not in st.session_state:
      source_journals = parse_COCI.parse_data(data)
      st.session_state['source_journals'] = source_journals
    else:
      source_journals = st.session_state['source_journals']
    st.header('Most important journals')
    source_journals = pd.DataFrame({'journals': source_journals.keys(), 'values': source_journals.values()})
    bars = alt.Chart(source_journals).mark_bar(size=20, align="center", binSpacing=1).encode(
        x=alt.X('journals', sort='-y'),
        y='values'
    ).properties(height=600)
    text = bars.mark_text(
        align='center',
        baseline='middle',
        color = 'white'
    ).encode(
        text='values')
    st.altair_chart(bars+text, use_container_width=True)
    st.write('''Top 10 of the most important journals for number of articles (either citing or cited) in the dataset.''')
  with col6:
    if 'source_fields' not in st.session_state:
      source_fields = parse_COCI.parse_data(data, asjc_fields=True)
      st.session_state['source_fields'] = source_fields
    else:
      source_fields = st.session_state['source_fields']
    st.header('Most important journals')
    st.header('''Most frequent academic fields''')
    source_fields = pd.DataFrame({'fields': source_fields.keys(), 'values': source_fields.values()})
    bars = alt.Chart(source_fields).mark_bar(size=20, align="center", binSpacing=0.5).encode(
        x=alt.X('fields', sort='-y'),
        y='values'
    ).properties(height=600)
    text = bars.mark_text(
        align='center',
        baseline='middle',
        color='white'
    ).encode(
        text='values')
    #(bars + text).properties(width=600, height=600)
    st.altair_chart(bars+text, use_container_width=True)
    st.write('''Top 10 of the most important fields for number of articles (either citing or cited) in the dataset.''')