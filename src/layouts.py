from dash import dcc, html
import dash_bootstrap_components as dbc


def create_layout(app):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                # Control Panel
                html.H4("Control Panel"),
                dcc.Upload(id='upload-data', children=html.Button('Upload Excel or CSV')),
                dcc.Dropdown(id='x-axis', placeholder="Select X axis"),
                dcc.Checklist(id='x-log-scale', options=[{'label': 'Log10 X axis', 'value': 'log'}], inline=True),
                dcc.Dropdown(id='y-axis', placeholder="Select Y axis"),
                dcc.Checklist(id='y-log-scale', options=[{'label': 'Log10 Y axis', 'value': 'log'}], inline=True),
                dcc.Dropdown(id='label-column', placeholder="Select label column"),
                
                # Theme Panel
                html.H4("Theme"),
                dcc.Dropdown(id='theme', options=[{'label': 'Light', 'value': 'light'}, {'label': 'Dark', 'value': 'dark'}]),
                dcc.Slider(id='point-size', min=1, max=20, value=5, marks={i: str(i) for i in range(1, 21)}),
                dcc.Input(id='point-color', type='text', placeholder='Color of the point'),

                # Annotation Panel
                html.H4("Annotating"),
                dcc.RadioItems(id='annotation-type', options=[{'label': 'By Ranking', 'value': 'rank'}, {'label': 'Manual', 'value': 'manual'}]),
                dcc.Input(id='ranking-top-n', type='number', placeholder='Top N points', value=10),
                dcc.Input(id='manual-genes', type='text', placeholder='Enter genes (comma separated)'),
                dcc.Input(id='annotation-color', type='text', placeholder='Annotation Color'),
            ], width=4),

            dbc.Col([
                # Plot Section
                html.H4("Figures"),
                dcc.Graph(id='interactive-figure'),
                html.Img(id='static-figure', src='', style={'width': '100%'})
            ], width=8)
        ])
    ])
