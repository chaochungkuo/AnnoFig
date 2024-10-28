import pandas as pd
import plotly.express as px
from io import StringIO
import base64


def parse_data(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(StringIO(decoded.decode('utf-8')))  # Modify if Excel
    return df

def generate_interactive_figure(df, x_col, y_col, x_log, y_log, label_col, point_size, point_color, theme):
    fig = px.scatter(df, x=x_col, y=y_col, text=label_col)
    
    if x_log:
        fig.update_layout(xaxis_type='log')
    if y_log:
        fig.update_layout(yaxis_type='log')
    
    fig.update_traces(marker=dict(size=point_size, color=point_color))
    
    if theme == 'dark':
        fig.update_layout(template='plotly_dark')
    
    return fig

def generate_static_figure(figure):
    file_path = 'static_figures/static_fig.png'
    figure.write_image(file_path, format='png', scale=3)  # Save as high-res PNG
    return file_path
