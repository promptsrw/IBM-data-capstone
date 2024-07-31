# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

pd.set_option('display.max_columns', None)
#print(spacex_df["Launch Site"].value_counts().index.tolist())
#site = ['CCAFS LC-40', 'KSC LC-39A', 'VAFB SLC-4E', 'CCAFS SLC-40']
#print(spacex_df.head())
#colu  = ['Flight Number', 'Launch Site', 'class', 'Payload Mass (kg)','Booster Version','Booster Version Category']
min_value = 0
max_value = max_payload
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                        100: '100'},
                                    value=[min_value, max_value]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='All sites')
        return fig
    else :
        filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
        class_pie = filtered_df["class"].value_counts().index.tolist()
        class_count = filtered_df["class"].value_counts().tolist()
        x = {'xclass':class_pie,'xcount':class_count}
        df_class = pd.DataFrame(x)
        #data = filtered_df.groupby('class')['class'].sum().reset_index()
        fig = px.pie(df_class, values='xcount', 
        names='xclass', 
        title=entered_site)
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site,value):
    print(value,type(value),'----------------------------')
    if entered_site == 'ALL':
        data = spacex_df[(spacex_df['Payload Mass (kg)'] > value[0]) 
                        & (spacex_df['Payload Mass (kg)'] < value[1]) ]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class',
        color="Booster Version Category",
        title='All sites')
        return fig
    else :
        data = spacex_df[spacex_df['Launch Site']== entered_site]
        data = data[(data['Payload Mass (kg)'] > value[0])
                        & (data['Payload Mass (kg)'] < value[1]) ]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class',
        color="Booster Version Category",
        title= entered_site)
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()

