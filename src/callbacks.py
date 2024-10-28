from dash import Input, Output, State
import pandas as pd
import plotly.express as px
from utils import parse_data, generate_interactive_figure, generate_static_figure


def register_callbacks(app):
    
    @app.callback(
        [Output('x-axis', 'options'), Output('y-axis', 'options'), Output('label-column', 'options')],
        [Input('upload-data', 'contents')],
        prevent_initial_call=True
    )
    def update_columns(file_content):
        df = parse_data(file_content)
        options = [{'label': col, 'value': col} for col in df.columns]
        return options, options, options

    @app.callback(
        Output('interactive-figure', 'figure'),
        [Input('x-axis', 'value'), Input('y-axis', 'value'), Input('x-log-scale', 'value'),
         Input('y-log-scale', 'value'), Input('label-column', 'value'), Input('point-size', 'value'),
         Input('point-color', 'value'), Input('theme', 'value')],
        [State('upload-data', 'contents')],
        prevent_initial_call=True
    )
    def update_interactive_figure(x_col, y_col, x_log, y_log, label_col, point_size, point_color, theme, file_content):
        df = parse_data(file_content)
        figure = generate_interactive_figure(df, x_col, y_col, x_log, y_log, label_col, point_size, point_color, theme)
        return figure

    @app.callback(
        Output('static-figure', 'src'),
        [Input('interactive-figure', 'figure')],
        prevent_initial_call=True
    )
    def update_static_figure(figure):
        static_img_path = generate_static_figure(figure)
        return static_img_path

