"""
This code is for making plot of GDP trends and CO2 emission (Gt CO2/ y) trends for 3 models with 3 scenarios.
The 3 models are: IMAGE, E3ME, GEM-E3;
the 3 scenrios are: Reference, COVID, Green (recovery) scenarios.

Author:    Hsing-Hsuan Chen
Created:   15.05.2021
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from mpl_axes_aligner import align

# Import files
read_file = pd.read_excel(r'X:\user\chenh\Python\Task_1B_Python\HH\CO2emission_202104.xlsx', sheet_name='CO2emission_2030')
read_2Deg = pd.read_excel(r'X:\user\chenh\Python\Task_1B_Python\HH\COMMIT 2C2020 scenario ranges.xlsx', sheet_name='read_data')
read_GDP = pd.read_excel(r'X:\user\chenh\Python\Task_1B_Python\HH\GDP_202104.xlsx', sheet_name='2015 Index_2030')

# CO2 Data of 2 degree scenario
read_2Deg['Scenarios']=read_2Deg['Model'].astype(str)+'_'+read_2Deg['Scenario']
read_2Deg.drop(['Model','Scenario','Region','Variable','Unit'], inplace=True, axis=1)
d2=read_2Deg.melt(id_vars="Scenarios",var_name="Year",value_name="Value")
d2=d2.sort_values(by=['Scenarios','Year'])
d2 = d2.pivot_table('Value', 'Year', 'Scenarios')
# Mt Co2 to Gt CO2
d2 = d2/1000

# CO2 Data of three models
read_file['Scenarios']=read_file['Model'].astype(str)+'_'+read_file['Scenario']
read_file.drop(['Model','Scenario','Region','Variable','Unit'], inplace=True, axis=1)

dd=read_file.melt(id_vars="Scenarios",var_name="Year",value_name="Value")
dd=dd.sort_values(by=['Scenarios','Year'])
dd = dd.pivot_table('Value', 'Year', 'Scenarios')
dd.rename(columns={'E3ME_REF':'Ref (E3ME)', 'E3ME_COVID':'COVID (E3ME)', 'E3ME_GREEN':'Green (E3ME)', \
                   'GEM-E3_REF':'Ref (GEM-E3)','GEM-E3_COVID':'COVID (GEM-E3)', 'GEM-E3_GREEN':'Green (GEM-E3)', \
                    'IMAGE_REF':'Ref (IMAGE)', 'IMAGE_COVID':'COVID (IMAGE)', 'IMAGE_GREEN':'Green (IMAGE)'}, inplace=True)
result= dd

# Dataframes for CO2 Plot 
E3ME_REFERENCE = result["Ref (E3ME)"]
E3ME_COVID = result["COVID (E3ME)"]
E3ME_GREEN = result["Green (E3ME)"]
GEME3_REFERENCE = result["Ref (GEM-E3)"]
GEME3_COVID = result["COVID (GEM-E3)"]
GEME3_GREEN = result["Green (GEM-E3)"]
IMAGE_REFERENCE = result["Ref (IMAGE)"]
IMAGE_COVID = result["COVID (IMAGE)"]
IMAGE_GREEN = result["Green (IMAGE)"]

minValue = d2[['AIM/CGE_2Deg2020', 'COPPE-COFFEE 1.0_2Deg2020','IMAGE 3.0_2Deg2020','POLES GECO2019_2Deg2020','PROMETHEUS_2Deg2020','REMIND-MAgPIE 1.7-3.0_2Deg2020','WITCH 5.0_2Deg2020']].min(axis=1).values[0]
maxValue = d2[['AIM/CGE_2Deg2020', 'COPPE-COFFEE 1.0_2Deg2020','IMAGE 3.0_2Deg2020','POLES GECO2019_2Deg2020','PROMETHEUS_2Deg2020','REMIND-MAgPIE 1.7-3.0_2Deg2020','WITCH 5.0_2Deg2020']].max(axis=1).values[0]
d2.rename(columns={'IMAGE 3.0_2Deg2020':'IMAGE_2Deg2020'}, inplace=True)
IMAGE_2Deg2020 = d2["IMAGE_2Deg2020"].values[0]

# GDP data
read_GDP['Scenarios']=read_GDP['Model'].astype(str)+'_'+read_GDP['Scenario']
read_GDP.drop(['Model','Scenario','Region','Variable','Unit'], inplace=True, axis=1)
d3=read_GDP.melt(id_vars="Scenarios",var_name="Year",value_name="Value")
d3=d3.sort_values(by=['Scenarios','Year'])
d3 = d3.pivot_table('Value', 'Year', 'Scenarios')
d3.rename(columns={'E3ME_REF':'E3ME_Ref', 'E3ME_COVID':'E3ME_COVID', 'E3ME_GREEN':'E3ME_Green', \
                   'GEM-E3_REF':'GEM-E3_Ref','GEM-E3_COVID':'GEM-E3_COVID', 'GEM-E3_GREEN':'GEM-E3_Green', \
                       'IMAGE_REF':'IMAGE_Ref', 'IMAGE_COVID':'IMAGE_COVID', 'IMAGE_GREEN':'IMAGE_Green'}, inplace=True)
# Dataframes for GDP Plot
E3ME_REFERENCE_GDP = d3["E3ME_Ref"]
E3ME_COVID_GDP = d3["E3ME_COVID"]
E3ME_GREEN_GDP = d3["E3ME_Green"]
GEME3_REFERENCE_GDP = d3["GEM-E3_Ref"]
GEME3_COVID_GDP = d3["GEM-E3_COVID"]
GEME3_GREEN_GDP = d3["GEM-E3_Green"]
IMAGE_REFERENCE_GDP = d3["IMAGE_Ref"]
IMAGE_COVID_GDP = d3["IMAGE_COVID"]
IMAGE_GREEN_GDP = d3["IMAGE_Green"]

# Making plot
fig, (ax2, ax1) = plt.subplots(1, 2, sharey=False)
plt.figure(figsize= (18.5, 21))
plt.title("", fontsize=20, fontweight="bold") 
ax1.set_ylim([19, 46])
# Min and Max of 2 degree scenarios to show on the plot
p1= (minValue-19)/(46-19)
p2=(maxValue-19)/(46-19)

# CO2 subplot
IMAGE_REFERENCE.plot(ax=ax1, title= '(b)', style='tab:blue', linestyle= '-.', linewidth = '2')
GEME3_REFERENCE.plot(ax=ax1, style='tab:blue', linewidth = '2.3')
E3ME_REFERENCE.plot(ax=ax1, style='tab:blue', linestyle= '--', linewidth = '2.1')

IMAGE_COVID.plot(ax=ax1, style='tab:red', linestyle= '-.', linewidth = '2.1')
GEME3_COVID.plot(ax=ax1, style='tab:red', linewidth = '2.3')
E3ME_COVID.plot(ax=ax1, style='tab:red', linestyle= '--', linewidth = '2.1')

IMAGE_GREEN.plot(ax=ax1, style='tab:green', linestyle= '-.', linewidth = '2.1')
GEME3_GREEN.plot(ax=ax1, style='tab:green', linewidth = '2.3')
E3ME_GREEN.plot(ax=ax1, style='tab:green', linestyle='--', linewidth = '2.1')

# Adding 2 degree scenario with a range bar and a dot
range= ax1.axvline(2030.5, p1,p2, label='Range 2 degree scenarios', color='gray', linewidth = '8', alpha=0.7)
dot1= ax1.scatter(2030.5, IMAGE_2Deg2020, label='2 degree scenario', linestyle='None',linewidth = '3', marker='o')

# Blue shade for Reference scenarios
ax1.fill_between(result.index, result['Ref (E3ME)'], result['Ref (IMAGE)'],
    color=(0.1, 0.5, 0.9), alpha=0.2)
# Red shade for COVID scenarios
ax1.fill_between(result.index, result['COVID (E3ME)'], result['COVID (IMAGE)'],
    color=(0.8, 0.1, 0.2), alpha=0.2)
# Green shade for Green scenarios
ax1.fill_between(result.index, result['Green (E3ME)'], result['Green (IMAGE)'],
    color=(0.8, 0.9, 0.5), alpha=0.2)


ylab = ax1.set_ylabel('CO\u2082 emissions (Gt CO\u2082/yr)', fontsize=22)
xlab = ax1.set_xlabel(None)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)

# GDP subplot
IMAGE_REFERENCE_GDP.plot(ax=ax2, title= '(a)', style='tab:blue', linestyle= '-.', linewidth = '2')
GEME3_REFERENCE_GDP.plot(ax=ax2, style='tab:blue', linewidth = '2')
E3ME_REFERENCE_GDP.plot(ax=ax2, style='tab:blue', linestyle= '--', linewidth = '2')

IMAGE_COVID_GDP.plot(ax=ax2, style='tab:red', linestyle= '-.', linewidth = '2')
GEME3_COVID_GDP.plot(ax=ax2, style='tab:red', linewidth = '2')
E3ME_COVID_GDP.plot(ax=ax2, style='tab:red', linestyle= '--', linewidth = '2')

IMAGE_GREEN_GDP.plot(ax=ax2, style='tab:green', linestyle= '-.', linewidth = '2')
GEME3_GREEN_GDP.plot(ax=ax2, style='tab:green', linewidth = '2')
E3ME_GREEN_GDP.plot(ax=ax2, style='tab:green', linestyle='--', linewidth = '2')


ylab = ax2.set_ylabel('GDP MER (2015 index)', fontsize=22)
xlab = ax2.set_xlabel(None)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)

# Adjust range, grid, tick label and suplot titles
ax2.set_ylim([76, 184])
ax1.grid(which='major', axis='y', linestyle='--')
ax2.grid(which='major', axis='y', linestyle='--')
ax1.tick_params(labelsize=22)
ax2.tick_params(labelsize=22)
ax1.title.set_size(22)
ax2.title.set_size(22)
align.yaxes(ax1, 35, ax2, 140)

# legend
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

scenario_a = mpatches.Patch(color='tab:blue', label='Ref')
scenario_b = mpatches.Patch(color='tab:red', label='COVID')
scenario_c = mpatches.Patch(color='tab:green', label='Green')

line1 = Line2D([0], [0], color='black', linewidth=3, linestyle='-.',label='IMAGE')
line2 = Line2D([0], [0], color='black', linewidth=3, linestyle='-',label='GEM-E3')
line3 = Line2D([0], [0], color='black', linewidth=3, linestyle='--',label='E3ME')

fig.legend(handles=[scenario_a,scenario_b,scenario_c,line1,line2,line3,range,dot1], labels=['Ref','COVID','Green','IMAGE','GEM-E3','E3ME','Range 2 degree scenarios','2 degree scenario'],
            loc='lower center',frameon=False, bbox_to_anchor=(0.5, 0.001), ncol=3, fontsize=20)

# Adjust plot boundaries
fig.subplots_adjust(top=0.954, bottom=0.225, left= 0.04, right=0.992, wspace=0.11)

# Show and save plot
plt.show()
fig.savefig(os.path.join(r'X:\user\chenh\Python\Task_1B_Python\HH\Final figures\Global CO2 emissions & GDP_re.png'), dpi=1200, bbox_inches='tight')
