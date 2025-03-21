import pandas as pd
import plotly.express as px
from io import StringIO
import base64
import math
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from adjustText import adjust_text



      
def parse_data(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(StringIO(decoded.decode('utf-8')))  # Modify if Excel
    return df

def generate_interactive_figure(df, x_col, y_col,
                                x_log=False, x_revert=False,
                                y_log=False, y_revert=False, 
                                point_size=10, point_color='blue', theme='light',
                                label_col=None, annotate_col=None,
                                top_n=0, annotate_cutoff=None, annotate_revert=False, manual_genes='',
                                annotation_color='red', annotation_font_size=10, annotation_font_color='black', force_text=0.3):
    
    # fig = px.scatter(df, x=x_col, y=y_col, hover_name=label_col)
    if x_log:
        min_positive_value = df[df[x_col] > 0][x_col].min()
        df[x_col] = df[x_col].apply(lambda x: min_positive_value if x <= 0 else x)
    if y_log:
        min_positive_value = df[df[y_col] > 0][y_col].min()
        df[y_col] = df[y_col].apply(lambda x: min_positive_value if x <= 0 else x)
    if isinstance(point_color, dict) and 'hex' in point_color:
        point_color = point_color['hex']
    if isinstance(annotation_color, dict) and 'hex' in annotation_color:
        annotation_color = annotation_color['hex']
    if isinstance(annotation_font_color, dict) and 'hex' in annotation_font_color:
        annotation_font_color = annotation_font_color['hex']
    
    sel_labels = get_annotate_labels(df, top_n, annotate_col, label_col,
                                     annotate_revert, annotate_cutoff,
                                     manual_genes)
    
    # Add overlay layer for highlighted points with different color and text annotations
    if sel_labels and label_col:
        # Separate data into highlighted and non-highlighted
        highlighted_df = df[df[label_col].isin(sel_labels)]
        non_highlighted_df = df[~df[label_col].isin(sel_labels)]
        
        # Base layer for all points with default color and without text annotations
        fig = px.scatter(non_highlighted_df, x=x_col, y=y_col, hover_name=label_col)
        fig.update_traces(marker=dict(size=point_size, color=point_color), text=None)
        fig.add_scatter(
            x=highlighted_df[x_col],
            y=highlighted_df[y_col],
            mode='markers+text',
            marker=dict(size=point_size, color=annotation_color),
            text=highlighted_df[label_col],
            textposition="top center",
            textfont=dict(size=annotation_font_size*2, color=annotation_font_color),
            showlegend=False
        )
    else:
        fig = px.scatter(df, x=x_col, y=y_col, hover_name=label_col)
        fig.update_traces(marker=dict(size=point_size, color=point_color), text=None)
    
    # Apply log scaling if specified
    if x_log:
        fig.update_layout(xaxis_type='log')
    if y_log:
        fig.update_layout(yaxis_type='log')
    # Reverse axes if specified
    if x_revert:
        fig.update_layout(xaxis=dict(autorange='reversed'))
    if y_revert:
        fig.update_layout(yaxis=dict(autorange='reversed'))
        
    # Apply a clean theme and grid settings
    fig.update_layout(
        template='simple_white' if theme == 'light' else 'plotly_dark',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        font=dict(size=14)
    )
    return fig


def generate_static_figure(df, x_col, y_col, x_log=False, x_revert=False, y_log=False, y_revert=False, 
                           point_size=10, point_color='blue', theme='light',  width=600, height=600,
                           label_col=None, annotate_col=None,
                           top_n=0, annotate_cutoff=None, annotate_revert=False, manual_genes='',
                           annotation_color='red', annotation_font_size=10, annotation_font_color='black', force_text=0.3, dpi=300):
    extra_size = 1.2
    # Check if input data or necessary columns are missing, create a placeholder if so
    if df is None or df.empty or x_col is None or y_col is None:
        fig, ax = plt.subplots(figsize=((width/dpi)*extra_size, (height/dpi)*extra_size))
        placeholder_text = "Please define the input data and\nselect both X and Y axes."
        ax.text(0.5, 0.5, placeholder_text, ha='center', va='center', fontsize=10, color='grey')
        ax.set_axis_off()  # Hide axes for a cleaner look
        
        # Save the placeholder figure
        fig_path = "static_figure.png"
        plt.savefig(fig_path, dpi=dpi)
        plt.close(fig)
        return fig_path
    
    # Define color theme
    if theme == 'dark':
        plt.style.use('dark_background')
    else:
        plt.style.use('default')
    if x_log:
        min_positive_value = df[df[x_col] > 0][x_col].min()
        df[x_col] = df[x_col].apply(lambda x: min_positive_value if x <= 0 else x)
    if y_log:
        min_positive_value = df[df[y_col] > 0][y_col].min()
        df[y_col] = df[y_col].apply(lambda x: min_positive_value if x <= 0 else x)
    if isinstance(point_color, dict) and 'hex' in point_color:
        point_color = point_color['hex']
    if isinstance(annotation_color, dict) and 'hex' in annotation_color:
        annotation_color = annotation_color['hex']
    if isinstance(annotation_font_color, dict) and 'hex' in annotation_font_color:
        annotation_font_color = annotation_font_color['hex']
    # Prepare figure
    fig, ax = plt.subplots(figsize=((width/dpi)*extra_size, (height/dpi)*extra_size))  # Set square figure size
    
    sel_labels = get_annotate_labels(df, top_n, annotate_col, label_col,
                                     annotate_revert, annotate_cutoff,
                                     manual_genes)

    if label_col and sel_labels:
        # Separate data into highlighted and non-highlighted
        highlighted_df = df[df[label_col].isin(sel_labels)]
        non_highlighted_df = df[~df[label_col].isin(sel_labels)]
    
        # Plot non-highlighted points
        sns.scatterplot(x=x_col, y=y_col, data=non_highlighted_df, 
                        ax=ax, s=point_size,
                        color=point_color, 
                        label='Data Points', legend=False, edgecolor=None)

        # Plot highlighted points with a different color
        sns.scatterplot(x=x_col, y=y_col, data=highlighted_df, 
                        ax=ax, s=point_size,
                        color=annotation_color, 
                        label='Highlighted Points', legend=False)
        # Apply log scaling to the data if specified
        if x_log:
            ax.set_xscale('log')
        if y_log:
            ax.set_yscale('log')
        # Annotate highlighted points with repelling arrows
        texts = []
        for _, row in highlighted_df.iterrows():
            label_text = str(row[label_col]) if row[label_col] else ''
            label_text = label_text.replace('$', '')  # Remove any special characters
            texts.append(ax.text(row[x_col], row[y_col], label_text, fontsize=annotation_font_size, color=annotation_font_color))
        
        adjust_text(texts, force_points=0.4, force_text=force_text, 
                    expand_points=(1, 1), expand_text=(1, 1), 
                    arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))
    
    else:
        # Plot non-highlighted points
        sns.scatterplot(x=x_col, y=y_col, data=df, ax=ax, s=point_size,
                        color=point_color, label='Data Points', legend=False, edgecolor=None)
        # Apply log scaling to the data if specified
        if x_log:
            ax.set_xscale('log')
        if y_log:
            ax.set_yscale('log')
    
    # Reverse axes if specified
    if x_revert:
        ax.invert_xaxis()
    if y_revert:
        ax.invert_yaxis()
    
    # Customize plot aesthetics
    ax.grid(False)
    ax.set_facecolor('white' if theme == 'light' else 'black')
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)
    # Set axis labels and title with specific font sizes
    ax.set_xlabel(x_col, fontsize=7)
    ax.set_ylabel(y_col, fontsize=7)

    # Set tick label size
    ax.tick_params(axis='both', which='major', labelsize=5)  # Major ticks
    # ax.tick_params(axis='both', which='minor', labelsize=)  # Minor ticks
    ax.tick_params(axis='both', width=0.4) 
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    
    # plt.legend()
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    # Save the figure as a static image
    fig_path = "static_figure.png"
    plt.savefig(fig_path, dpi=dpi)
    plt.close(fig)  # Close the figure after saving
    
    return fig_path

def get_annotate_labels(df, top_n, annotate_col, label_col,
                        annotate_revert, annotate_cutoff, manual_genes):
    # Store the labels after filtering by different criteria
    sel_labels = []

    # Annotate based on the top N points in the annotate_col column
    if top_n > 0 and annotate_col in df.columns and label_col in df.columns:
        sorted_df = df.sort_values(by=annotate_col, ascending=not annotate_revert)
        sel_labels += sorted_df[label_col].head(top_n).tolist()
    
    # Annotate by the defined cutoff
    if annotate_cutoff is not None and annotate_col in df.columns and label_col in df.columns:
        if annotate_revert:
            sel_labels += df[df[annotate_col] > annotate_cutoff][label_col].tolist()
        else:
            sel_labels += df[df[annotate_col] < annotate_cutoff][label_col].tolist()
    
    # Annotate manually entered genes
    if manual_genes:
        sel_labels += [gene.strip() 
                       for gene in manual_genes.replace(',', ' ').split()]
        
    sel_labels = list(set(sel_labels))  # Remove duplicates
    return sel_labels

# Using base64 encoding and decoding
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')