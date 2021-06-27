import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import data
read_file = pd.read_excel(r'X:\user\chenh\Python\Task_1B_Python\HH\Energy_indicator_202104.xlsx', sheet_name='Few_ind2')

# Rename scenarios, models, regions
read_file['Scenario'] = read_file['Scenario'].replace(['EN_NPi2100','CurPol_Reference','REFERENCE','Dan_ba_precovid'],'Ref')
read_file['Scenario'] = read_file['Scenario'].replace(['EN_NPi2100_COV','Dan_ba','CurPol_CovidBaseline','COVID'],'COVID')
read_file['Scenario'] = read_file['Scenario'].replace(['DGCL_GREEN_COVID_v5','Dan_GR20','CurPol_GreenRecovery','GREEN'],'Green')
read_file['Model'] = read_file['Model'].replace(['GEM-E3_V2021','GEM-E3_v2021'],'GEM-E3')
read_file['Variable'] = read_file['Variable'].replace(['Final Energy|Residential and Commercial'],'(b) Final Energy|Buildings')
read_file['Variable'] = read_file['Variable'].replace(['Final Energy|Industry'],'(a) Final Energy|Industry')
read_file['Variable'] = read_file['Variable'].replace(['RES share'],'(c) Renewables in electricity')
read_file['Variable'] = read_file['Variable'].replace(['EV share'],'(d) Electric vehicles')

# Transform Scenario and Year+Scenario to categorical type, which means they can be ordered
read_file.set_index(['Model', 'Scenario','Variable'])
read_file.drop(['Region','Unit'], inplace=True, axis=1)
data= read_file
data_reset = data.set_index(['Model', 'Scenario', 'Variable']).rename_axis('Year', axis=1).stack().reset_index().rename(columns={0: 'Value'})
data_reset['Year+Scenario'] = data_reset['Year']+'+'+data_reset['Scenario']
average_reset = data_reset.groupby(['Scenario', 'Variable', 'Year', 'Year+Scenario']).mean().reset_index()
data_reset = data.set_index(['Model', 'Scenario', 'Variable']).rename_axis('Year', axis=1).stack().reset_index().rename(columns={0: 'Value'})

data_reset['Scenario'] = pd.Categorical(data_reset['Scenario'], ['Ref', 'COVID', 'Green'], ordered=True)
data_reset['Variable'] = pd.Categorical(data_reset['Variable'], ['(a) Final Energy|Industry', '(b) Final Energy|Buildings','(c) Renewables in electricity','(d) Electric vehicles'])
data_reset.sort_values("Variable")
data_reset['Model'] = pd.Categorical(data_reset['Model'], ['GEM-E3', 'IMAGE', 'E3ME'])
data_reset.sort_values("Model")
data_reset['Year+Scenario'] = pd.Categorical(
    data_reset['Year']+'+'+data_reset['Scenario'].astype(str),
    [f'{y}+{s}' for y in data_reset['Year'].sort_values().unique() for s in data_reset['Scenario'].cat.categories],
    ordered=True
)

average_reset = data_reset.groupby(['Scenario', 'Variable', 'Year', 'Year+Scenario']).mean().reset_index()

# Sort values of both dataframes
average_reset = average_reset.sort_values(['Variable', 'Year+Scenario'])
data_reset = data_reset.sort_values(['Variable', 'Year+Scenario'])

# Create a first figure with the bars
fig = px.bar(
    average_reset,
    x='Year+Scenario', y='Value', color='Scenario', opacity=0.6, facet_col='Variable', facet_col_wrap=2,
    facet_row_spacing=0.25
)

# Create a second figure with the points per model
fig2 = px.scatter(
    data_reset,
    x='Year+Scenario', y='Value', symbol='Model',symbol_map={'IMAGE': 'x-thin-open', 'GEM-E3': 'circle-open', 'E3ME': 'cross-thin-open'}, facet_col='Variable', facet_col_wrap=2,
    facet_row_spacing=0.25
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
        height=800, width=800, title= '', legend_title=''
    )
    .update_xaxes(showticklabels=True, title='')
    .update_yaxes(title='Final energy use relative to 2015 (%)', row=2,col=1, titlefont_size=15)
    .update_yaxes(title='Share (% of total)', row=1,col=1, titlefont_size=15)
    .for_each_annotation(lambda ann: ann.update(text=ann.text.split('Variable=')[1]))
    .update_layout(font_size=15)
)


# Save and show the plot
fig.show()
fig.write_image(r'X:\user\chenh\Python\Task_1B_Python\HH\\Final figures\Energy indicators.png', scale=5)