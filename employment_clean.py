
"""
This code is aim to make staked bar charts for 2 models, show the employment changes between COVID and Green scenrios.
The 3 models are: E3ME, GEM-E3.

Author:    Hsing-Hsuan Chen
Created:   17.06.2021
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Import data
read_GEME3 = pd.read_excel(r'X:\user\chenh\CLIMA_2020\7_Reporting_Tool\Employment_data_GEME3.xlsx', sheet_name='data',header=0)
read_E3ME = pd.read_excel(r'X:\user\chenh\CLIMA_2020\7_Reporting_Tool\E3ME employment by sectors_summary.xlsx', sheet_name='data',header=0)

# Set index and transpose datasets
read_GEME3.set_index('Sector', inplace=True)
read_E3ME.set_index('Sector', inplace=True)
read_GEME3_reset = read_GEME3.transpose()
read_E3ME_reset = read_E3ME.transpose()

# Making staked bar chart
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
read_E3ME_reset.plot(ax=ax1, title='E3ME', kind='bar',ylabel='Million jobs differences', stacked=True, legend= False)
read_GEME3_reset.plot(ax=ax2, title='GEM-E3-FIT', kind='bar', stacked=True, legend= False)

# Set y range
ax1.set_ylim([-4.5, 13.5])
ax2.set_ylim([-4.5, 13.5])

# Add legend
plt.legend(['Agriculture', 'Fossil fuels','Electricity','Construction','Industries','Services','Clean manufac'], loc = 'lower center', bbox_to_anchor = (0,0,1,1), ncol=4,
            bbox_transform = plt.gcf().transFigure)

fig = plt.gcf()

# Adjust the plot boundaries 
plt.subplots_adjust(top=0.86, bottom=0.22, left= 0.11, right=0.9)

# Show plot
plt.show()