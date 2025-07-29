import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=100),
    "Sales": np.random.randint(100, 500, size=100),
    "Region": np.random.choice(["North", "South", "East", "West"], size=100)
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Dashboard with Filters"),

    # Date range picker component
    dcc.DatePickerRange(
        id='date-range',
        start_date=df['Date'].min(),
        end_date=df['Date'].max(),
        display_format='YYYY-MM-DD'
    ),

    # Multi-select dropdown for regions
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': r, 'value': r} for r in df['Region'].unique()],
        value=df['Region'].unique().tolist(),
        multi=True
    ),

    # Graph component to display sales plot
    dcc.Graph(id='sales-graph')
])

@app.callback(
    Output('sales-graph', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('region-dropdown', 'value')
)
def update_graph(start_date, end_date, selected_regions):
    # Filter data by selected dates and regions
    filtered_df = df[
        (df['Date'] >= pd.to_datetime(start_date)) &
        (df['Date'] <= pd.to_datetime(end_date)) &
        (df['Region'].isin(selected_regions))
    ]

    # Create the line chart with filtered data
    fig = px.line(
        filtered_df, 
        x='Date', 
        y='Sales', 
        color='Region',
        title='Sales Over Time by Region'
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
