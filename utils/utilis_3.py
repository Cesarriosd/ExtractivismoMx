import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd

# Sample data (replace with your data or load from a CSV/database)
data = {
    "Poblado": ["La ventosa", "Alvaro Obregón", "Jalcomulco"],
    "Extractivista": ["Acciona", "NA", "Odebrecht"],
    "Latitude": [16.552777777778 , 16.297222, 19.331944],
    "Longitude": [-94.947222222222, -95.084722,  -96.7625],
    "Population": [8918653, 1495182, 1135512],
    "Category": ["Parque Eólico", "Parque Eólico", "Presa"],
}
df_columns_of_interest = ["Poblado", "Extractivista", "Category"]
# Create a DataFrame
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("ExtractivismoMx", style={"textAlign": "center"}),
    
    # Filters section (side by side)
    html.Div([
        # Category Filter
        html.Div([
            html.Label("Poblado:"),
            dcc.Dropdown(
                id="Poblado-filtro",
                options=[{"label": cat, "value": cat} for cat in df["Poblado"].unique()],
                value=None,
                multi=True,
                placeholder="Selecciona un poblado"
            ),
        ], style={"width": "48%", "display": "inline-block", "marginRight": "2%"}),
        
        # City Filter
        html.Div([
            html.Label("Empresa Extractivista:"),
            dcc.Dropdown(
                id="Extractivista-filtro",
                options=[{"label": empresa, "value": empresa} for empresa in df["Extractivista"].unique()],
                value=None,
                multi=True,
                placeholder="Selecciona una empresa"
            ),
        ], style={"width": "48%", "display": "inline-block"}),
    ], style={"margin": "20px", "display": "flex"}),  # Use flexbox for side-by-side layout
    
    # Main content: Map on the left, Table on the right
    html.Div([
        # Map
        html.Div(
            dcc.Graph(id="mexico-map"),
            style={"width": "50%", "display": "inline-block"}
        ),
        
        # Table
        html.Div(
            dash_table.DataTable(
                id="data-table",
                columns=[{"name": col, "id": col} for col in df_columns_of_interest],
                data=df.to_dict("records"),
                style_table={"height": "600px", "overflowY": "auto"},
                style_cell={"textAlign": "left", "padding": "10px"},
                style_header={"backgroundColor": "lightgray", "fontWeight": "bold", "textAlign": "left", "padding": "10px", "fontFamily": "Arial, sans-serif"},
            ),
            style={"width": "50%", "display": "inline-block", "padding": "20px"}
        ),
    ], style={"display": "flex"}),
])

# Callback to update the map and table based on filters
@app.callback(
    [Output("mexico-map", "figure"),
     Output("data-table", "data")],
    [Input("Poblado-filtro", "value"),
     Input("Extractivista-filtro", "value")]
)
def update_dashboard(selected_categories, selected_cities):
    # Filter data based on selected categories
    filtered_df = df.copy()
    if selected_categories:
        filtered_df = filtered_df[filtered_df["Poblado"].isin(selected_categories)]
    
    # Filter data based on selected cities
    if selected_cities:
        filtered_df = filtered_df[filtered_df["Extractivista"].isin(selected_cities)]
    
    # Create the map with colors based on the Category column
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Poblado",
        hover_data=["Population", "Category"],
        color="Category",  # Color points by the Category column
        color_discrete_map={
        "Parque Eólico": "rgb(15,189,242)",
        "Presa": "red"
        },
        zoom=4,
        height=600,
        title="Map of Mexico"
    )
    
    # Customize the map style
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    
    # Update the table data
    table_data = filtered_df.to_dict("records")
    
    return fig, table_data

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)