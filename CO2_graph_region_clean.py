
"""
This code is aim to make regional CO2 emisiion plots, for 3 models with 3 scenarios.
The 3 models are: IMAGE, E3ME, GEM-E3;
the 3 scenrios are: Reference, COVID, Green (recovery) scenarios.

Author:    Hsing-Hsuan Chen
Created:   17.06.2021
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import file
read_file = pd.read_excel(r'X:\user\chenh\Python\Task_1B_Python\HH\Regional_CO2emission_202104.xlsx', sheet_name='2015 index_no KOR')

# Rename scenarios, models, regions
read_file['Scenario'] = read_file['Scenario'].replace(['EN_NPi2100','CurPol_Reference','Dan_ba_precovid'],'Ref')
read_file['Scenario'] = read_file['Scenario'].replace(['EN_NPi2100_COV','Dan_ba','CurPol_CovidBaseline'],'COVID')
read_file['Scenario'] = read_file['Scenario'].replace(['DGCL_GREEN_COVID_v5','Dan_GR20','CurPol_GreenRecovery'],'Green')
read_file['Model'] = read_file['Model'].replace(['GEM-E3_V2021'],'GEM-E3')
read_file['Region'] = read_file['Region'].replace(['CN','CHN'],'(b) CHN')
read_file['Region'] = read_file['Region'].replace(['US','USA'],'(e) USA')
read_file['Region'] = read_file['Region'].replace(['JA','JPN','JAP'],'(d) JAP')
read_file['Region'] = read_file['Region'].replace(['IN','INDIA','IND'],'(c) IND')
read_file['Region'] = read_file['Region'].replace(['BR','BRA'],'(a) BRA')
read_file['Region'] = read_file['Region'].replace(['WEU','EU_28','EU28'],'(f) EU28')
read_file.set_index(['Model', 'Scenario','Region'])
read_file.drop(['Variable','Unit','2015','2020'], inplace=True, axis=1)
data= read_file

# Transform Scenario and Year+Scenario to categorical type, which means they can be ordered
data_reset = data.set_index(['Model', 'Scenario', 'Region']).rename_axis('Year', axis=1).stack().reset_index().rename(columns={0: 'Value'})
data_reset['Year+Scenario'] = data_reset['Year']+'+'+data_reset['Scenario']
average_reset = data_reset.groupby(['Scenario', 'Region', 'Year', 'Year+Scenario']).mean().reset_index()
data_reset = data.set_index(['Model', 'Scenario', 'Region']).rename_axis('Year', axis=1).stack().reset_index().rename(columns={0: 'Value'})

data_reset['Scenario'] = pd.Categorical(data_reset['Scenario'], ['Ref', 'COVID', 'Green'], ordered=True)
data_reset['Year+Scenario'] = pd.Categorical(
    data_reset['Year']+'+'+data_reset['Scenario'].astype(str),
    [f'{y}+{s}' for y in data_reset['Year'].sort_values().unique() for s in data_reset['Scenario'].cat.categories],
    ordered=True
)

average_reset = data_reset.groupby(['Scenario', 'Region', 'Year', 'Year+Scenario']).mean().reset_index()


# Create a first figure with the bars
fig = px.bar(
    average_reset,
    x='Year+Scenario',
    y='Value', color='Scenario',
    opacity=0.6, facet_col='Region',
    facet_col_wrap=3,
    category_orders={"Region": ['(a) BRA','(b) CHN','(c) IND','(d) JAP','(e) USA','(f) EU28']},
    facet_row_spacing=0.25
)

# Create a second figure with the points per model
fig2 = px.scatter(
    data_reset,
    x='Year+Scenario',
    y='Value', symbol='Model',
    symbol_sequence= ['circle-open', 'x-thin-open', 'cross-thin-open'],
    facet_col='Region', facet_col_wrap=3,
    category_orders={"Region": ['(a) BRA','(b) CHN','(c) IND','(d) JAP','(e) USA','(f) EU28']}
)

for trace in fig2.data: # Take each trace from fig2, and add it to the main fig
    fig.add_trace(trace.update(marker_color='black'))

def split_yearscenario(xvalues):
    return np.array([x.split('+') for x in xvalues]).T
fig = (
    fig
    .for_each_trace( # Update the year+scenario to multicategory axis
        lambda trace: trace.update(x=split_yearscenario(trace.x))
    )
    .update_layout(
        height=650, width=800, title= '', legend_title='', font_size= 14
    )
    .update_xaxes(showticklabels=True, title='')
    .update_yaxes(matches=None)
    .update_yaxes(range=[-50, 10], row=1)
    .update_yaxes(range=[-10, 80], row=2)   
    .update_yaxes(
        tickmode = 'linear',
        dtick = 10
    )    
    .update_yaxes(title='')
    .update_yaxes(title='CO\u2082 emissions relative to 2015 (%)', col=1)
    .update_yaxes(tickfont_size=14)
    .update_xaxes(tickfont_size=14)

    .for_each_annotation(lambda ann: ann.update(text=ann.text.split('Region=')[1],font_size=15))
    .for_each_yaxis(lambda axis: axis.title.update(font=dict(size=15)))
)


# Save and show the plot
fig.write_image(r'X:\user\chenh\Python\Task_1B_Python\HH\Final figures\Regional CO2 emissions_0617.png', scale=5)
fig.show()