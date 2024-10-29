from dash import Input, Output, State
import pandas as pd
import plotly.express as px
from utils import parse_data, generate_interactive_figure, generate_static_figure
import base64
import io
from dash import html


def register_callbacks(app):
    
    @app.callback(
        [Output('x-axis', 'options'), Output('y-axis', 'options'),
         Output('label-column', 'options'), Output('annotate-column', 'options')],
        [Input('upload-data', 'contents')],
        prevent_initial_call=True
    )
    def update_columns(file_content):
        df = parse_data(file_content)
        options = [{'label': col, 'value': col} for col in df.columns]
        return options, options, options, options

    @app.callback(
        Output('interactive-figure', 'figure'),
        [Input('x-axis', 'value'), Input('y-axis', 'value'),
        Input('x-log-scale', 'value'), Input('x-revert', 'value'),
        Input('y-log-scale', 'value'), Input('y-revert', 'value'),
        Input('point-size', 'value'),
        Input('point-color', 'value'), Input('theme', 'value'),
        Input('label-column', 'value'), Input('annotate-column', 'value'), 
        Input('ranking-top-n', 'value'), Input('annotate-cutoff', 'value'),
        Input('annotate-revert', 'value'), Input('manual-genes', 'value'),
        Input('annotation-color', 'value')],
        [State('upload-data', 'contents')],
        prevent_initial_call=True
    )
    def update_interactive_figure(x_col, y_col, x_log, x_revert, y_log, y_revert,
                                  point_size, point_color, theme,
                                  label_col, annotate_col, 
                                  top_n, annotate_cutoff,
                                  annotate_revert, manual_genes, annotation_color, file_content):
        df = parse_data(file_content)
        figure = generate_interactive_figure(
            df, x_col, y_col, x_log, x_revert, y_log, y_revert, 
            point_size, point_color, theme, label_col, annotate_col,
            top_n, annotate_cutoff, annotate_revert, manual_genes, annotation_color
        )
        return figure

    @app.callback(
        Output('static-figure', 'src'),
        [Input('x-axis', 'value'), Input('y-axis', 'value'),
        Input('x-log-scale', 'value'), Input('x-revert', 'value'),
        Input('y-log-scale', 'value'), Input('y-revert', 'value'),
        Input('point-size', 'value'),
        Input('point-color', 'value'), Input('theme', 'value'),
        Input('width', 'value'), Input('height', 'value'),
        Input('label-column', 'value'), Input('annotate-column', 'value'), 
        Input('ranking-top-n', 'value'), Input('annotate-cutoff', 'value'),
        Input('annotate-revert', 'value'), Input('manual-genes', 'value'),
        Input('annotation-color', 'value')],
        [State('upload-data', 'contents')],
        prevent_initial_call=True
    )
    def update_static_figure(x_col, y_col, x_log, x_revert, y_log, y_revert,
                             point_size, point_color, theme, width, height,
                             label_col, annotate_col, 
                             top_n, annotate_cutoff,
                             annotate_revert, manual_genes, annotation_color, file_content):
        df = parse_data(file_content)
        static_img_path = generate_static_figure(
            df, x_col, y_col, x_log, x_revert, y_log, y_revert, 
            point_size, point_color, theme,  width, height, label_col, annotate_col,
            top_n, annotate_cutoff, annotate_revert, manual_genes, annotation_color
        )
        static_img_path = 'data:assets/png;base64,{}'.format(base64.b64encode(
                open(
                    static_img_path, 'rb'
                ).read()
            ).decode()
                            )
        return static_img_path

    # Callback to process the uploaded file and display its info
    @app.callback(
        Output('file-info', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def update_file_info(contents, filename):
        if contents is None:
            return ""
        
        # Decode the uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Check file type and load data
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(io.BytesIO(decoded), sheet_name=0)
            else:
                return "Unsupported file format"
            
            # Get the number of rows
            row_count = len(df)
            
            # Display the filename and row count
            return [f"File: {filename}", html.Br(), f"Rows: {row_count}"]
        except Exception as e:
            return f"Error processing file: {str(e)}"
        
    # Callback to update the width and height of both figures
    @app.callback(
        [Output('interactive-figure', 'style'),
        Output('static-figure', 'style')],
        [Input('width', 'value'),
        Input('height', 'value')]
    )
    def update_figure_size(width, height):
        # Define the style dictionaries with dynamic width and height
        new_style = {
            'width': f'{width}px' if width else '600px',  # Default to 600px if None
            'height': f'{height}px' if height else '600px'  # Default to 600px if None
        }
        return new_style, new_style