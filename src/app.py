from dash import Dash
from layouts import create_layout
from callbacks import register_callbacks
import dash_bootstrap_components as dbc
# import os

external_stylesheets = [dbc.themes.CERULEAN]
# Initialize Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets,
           url_base_pathname='/annofig/')

# Set layout
app.layout = create_layout(app_title="AnnoFig")

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8051)
