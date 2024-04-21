import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from util import get_index_pairs, get_json_data
import time

np.random.seed(42)
n_points = 184
start_time = datetime.now() - timedelta(hours=n_points)

json_data = get_json_data()

hanoi_data = {
    # 'Time': [start_time + timedelta(hours=i) for i in range(n_points)] * 10,
    'Index': [item['Index'] for item in json_data],
    'Tram': [item['Tram'] for item in json_data],
    'Latitude': [float(item['Latitude']) for item in json_data],
    'Longitude': [float(item['Longitude']) for item in json_data],
    'PM2.5': np.random.uniform(0, 50, 184),
    'BaoDong': np.random.choice([0, 0], 184)
}

hanoi_df = pd.DataFrame(hanoi_data)

print("Load xong Thông tin về trạm")

def create_map(df):
    # Create a scatter mapbox with plotly
    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="BaoDong", size="PM2.5",
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                            mapbox_style="carto-positron")

    return fig

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1('Heatmap of Hanoi'),
    dcc.Graph(id='live-map'),
    html.Button('Update', id='update-button'),
])

# Define the callback to update the map
@app.callback(Output('live-map', 'figure'),
              Input('update-button', 'n_clicks'))
def update_map(n):
    if n is None:
        # Don't update the data_web if the button hasn't been clicked
        raise dash.exceptions.PreventUpdate

    # Update data_web
    hanoi_df['PM2.5'] = np.random.uniform(0, 50, 184)
    hanoi_df['BaoDong'] = np.random.choice([0, 1], 184)

    # Create map
    my_map = create_map(hanoi_df)
    print("Tạo xong bản đồ !!!")

    return my_map

if __name__ == '__main__':
    app.run_server(debug=True)

