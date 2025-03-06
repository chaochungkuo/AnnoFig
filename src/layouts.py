from dash import dcc, html
import dash_bootstrap_components as dbc
import base64
import dash_daq as daq
from utils import b64_image



def create_layout(app_title):
    return dbc.Container([
        create_banner(app_title=app_title),
        dbc.Row([
            dbc.Col([
                html.H1("AnnoFig"),
                html.Div("Annotating your figure as you want."),
                html.Div("When there are too many data points, every updating might take a few seconds to process. If error occurs, please contact chao-chung.kuo@rwth-aachen.de or refresh the page."),
                html.Br(),
                # Control Panel
                html.H3("Control Panel"),
                dcc.Upload(id='upload-data', children=html.Button('Upload CSV file')),
                html.Div(id='file-info'),  # Div to display file name and row count
                html.Div("Select the columns for X axis:"),
                dcc.Dropdown(id='x-axis', placeholder="Select X axis"),
                dcc.Checklist(id='x-log-scale', options=[{'label': 'Log10 X axis', 'value': 'log'}], inline=False),
                dcc.Checklist(id='x-revert', options=[{'label': 'Revert X axis', 'value': 'revert'}], inline=False),
                html.Div("Select the columns for Y axis:"),
                dcc.Dropdown(id='y-axis', placeholder="Select Y axis"),
                dcc.Checklist(id='y-log-scale', options=[{'label': 'Log10 Y axis', 'value': 'log'}], inline=False),
                dcc.Checklist(id='y-revert', options=[{'label': 'Revert Y axis', 'value': 'revert'}], inline=False),
                html.Br(),
                
                # Theme Panel
                html.H3("Theme"),
                dcc.Dropdown(id='theme', 
                             options=[{'label': 'Light', 'value': 'light'},
                                      {'label': 'Dark', 'value': 'dark'}],
                             value="light"),
                html.Div("Change the size of the data points"),
                dcc.Slider(id='point-size', min=1, max=20, value=4, marks={i: str(i) for i in range(1, 21)}),
                html.Div("Change the color of the data points"),
                daq.ColorPicker(
                    id='point-color',
                    label='Color Picker',
                    value=dict(hex='#119DFF')
                ),
                html.Div("Change the size of the figures"),
                html.Div("Width:"),
                dcc.Input(id='width', type='number', placeholder='Define the width', value=600),
                html.Div("Height:"),
                dcc.Input(id='height', type='number', placeholder='Define the height', value=600),
                html.Br(),
                html.Br(),

                # Annotation Panel
                html.H3("Annotating"),
                html.Div("Select the labels to show:"),
                dcc.Dropdown(id='label-column', placeholder="Select label column (e.g. Gene name)"),
                html.Div("Select the column to filter:"),
                dcc.Dropdown(id='annotate-column', 
                             placeholder="Select a column to filter (e.g. adjusted p-values)"),
                html.Div("Filtering data points for annotation"),
                html.Div("by defining a cutoff:"),
                dcc.Input(id='annotate-cutoff', type='number',
                          placeholder='Define a cutoff', value=None),
                html.Div("or, by their ranking:"),
                dcc.Input(id='ranking-top-n', type='number', 
                          placeholder='Top N points', value=0),
                dcc.Checklist(id='annotate-revert', options=[{'label': 'Revert the ranking of annotated column', 'value': 'annotate-revert'}], inline=False),
                dcc.Input(id='manual-genes', type='text', 
                          placeholder='Enter genes (comma or space separated)'),
                html.Div("Define the color of the annotated data points"),
                daq.ColorPicker(
                    id='annotation-color',
                    label='Color Picker',
                    value=dict(hex='#FF8711')
                ),
                html.Div("Define the font size of the annotated labels"),
                dcc.Slider(id='annotation-font-size', min=5, max=20, value=7,
                           marks={i: str(i) for i in range(5, 21)}),
                html.Div("Define the font color of the annotated labels"),
                daq.ColorPicker(
                    id='annotation-font-color',
                    label='Color Picker',
                    value=dict(hex='#000000')
                ),
                html.Div("Control the repelling force for text annotations"),
                dcc.Input(id='force-text', type='number',
                          placeholder='Enter repelling force', value=0.3, step=0.1),
            ], width=4),

            dbc.Col([
                # Plot Section
                html.Div("Any adjustment in the control panel on the left will update the figures below automatically."),
                html.H3("Interactive Figure"),
                html.Div("Labels won't be applied to the interactive figure, because interactive figure is used to explore the data by hovering the data points."),
                dcc.Graph(id='interactive-figure', style={'width': '600px', 'height': '600px'}),
                html.Br(),
                html.H3("Static Figure"),
                html.Img(id='static-figure',
                         src=b64_image('./assets/static_figure.png'),
                         alt='Please define the input data and\nselect both X and Y axes.',
                         style={'width': '600px', 'height': '600px'})
            ], width=8)
        ])
    ])


def create_banner(app_title):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(src=b64_image('./assets/plotly_logo.png'),
                                     style={'height': '40px'}), width=10),
                    dbc.Col(html.A(
                        id='gh-link',
                        children=[
                            'View on GitHub'
                        ],
                        href="https://github.com/chaochungkuo/AnnoFig",
                        style={'color': 'black'}
                    ))
                ], justify="start")
        ],
        style={'padding': '0.5em'},
    )


