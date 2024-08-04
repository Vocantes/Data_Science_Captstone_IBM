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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                               html.Label("Select Site Location"),
                                html.Div(
                                    dcc.Dropdown(id="site-dropdown",
                                    options=[{"label":"All Sites","value":"ALL"},
                                    {"label":"CCAFS LC-40","value":"CCAFS LC-40"},
                                    {"label":"CCAFS SLC-40","value":"CCAFS SLC-40"},
                                    {"label":"KSC LC-39A","value":"KSC LC-39A"},
                                    {"label":"VAFB SLC-4E","value":"VAFB SLC-4E"}],value="ALL",placeholder="Select Launch Site",searchable=True)
                                    ),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                html.Div(
                                    dcc.RangeSlider(id="payload-slider",min=0,max=10000, step=1000,value=[min_payload,max_payload])
                                    ),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback(
    Output("success-pie-chart",component_property="figure"),
    Input("site-dropdown","value")
)
def get_pie(value):
    if value == "ALL":
        pie_df = spacex_df["class"].value_counts().to_frame()
        pie_graph = px.pie(pie_df,values="count",names=["Failure","Success"],title="Pie Chart for Success and Failures for All Sites")
    else:
        pie_df = spacex_df[spacex_df["Launch Site"] == value]["class"].value_counts().to_frame()
        if value == "KSC LC-39A":
            names = ["Success","Failure"]
        else:
            names = ["Failure","Success"]
        pie_graph = px.pie(pie_df,values="count",names=names,title= f"Pie Chart for Success and Failures for {value}")
    #print(pie_df)
    return pie_graph

@app.callback(
    Output("success-payload-scatter-chart","figure"),
    [Input("site-dropdown","value"),
    Input("payload-slider","value")]
)

def payload_graph_update(launch_site, slider_value):
    if launch_site == "ALL":
        scatter_df = spacex_df
    else:
        scatter_df = spacex_df[spacex_df["Launch Site"] == launch_site]
    scatter_df = scatter_df[(scatter_df["Payload Mass (kg)"] > slider_value[0]) & (spacex_df["Payload Mass (kg)"] < slider_value[1])]
    scatter_graph = px.scatter(data_frame=scatter_df,x="Payload Mass (kg)",y="class",color="Booster Version Category",title="Correlation between Payload Mass and Success")
    return scatter_graph

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
