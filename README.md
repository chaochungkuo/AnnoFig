# AnnoFig

A web app for annotating scatter plots.

**AnnoFig** is a Python-based data visualization tool built with Plotly Dash, Matplotlib, and Seaborn, designed to help researchers annotate and analyze figures interactively. AnnoFig allows users to upload datasets (Excel or CSV), configure plots with options like log scales, axis reversal, and highlight specific data points for custom annotation. It provides both interactive and static visualizations, making it suitable for both exploratory analysis and publication-ready figures.

[DEMO](https://genomics.rwth-aachen.de/annofig/)

## Key Features

- **Data Upload**: Supports CSV and Excel file uploads, automatically loading the first sheet from Excel files.
- **Configurable Axes**: Choose data columns for the X and Y axes, with options for log scaling and axis reversal.
- **Highlight and Annotate**:
  - Highlight points based on top values in a selected column.
  - Set cutoff thresholds or manually specify genes or data points for annotation.
- **Interactive and Static Figures**:
  - Interactive figures powered by Plotly Dash.
  - Static figures created with Matplotlib and Seaborn, including adjustable spacing and repelling text annotations to prevent label overlap.
- **Export Options**: Easily save figures in high-resolution formats for presentations and publications.

## Getting Started

### Prerequisites

- Python 3.7 or later
- Required libraries:
  - Dash
  - Plotly
  - Matplotlib
  - Seaborn
  - Pandas
  - `adjustText` (for repelling text annotations in Matplotlib)

Install all dependencies using:

```bash
pip install -r requirements.txt
```

### Installation

Clone the repository and navigate to the project folder:

```bash
git clone https://github.com/chaochungkuo/AnnoFig
cd AnnoFig
```

### Running the Application

Start the Dash app by running:

```bash
python app.py
```

Once started, the app will be accessible at `http://127.0.0.1:8050` in your web browser.

### Usage

1. **Upload a File**: Upload a CSV or Excel file with your data. The file information, including name and row count, will be displayed.
2. **Configure the Plot**:
   - Select X and Y axes from dropdown menus.
   - Apply log scaling and axis reversal as needed.
3. **Annotation Options**:
   - Use dropdowns and checkboxes to highlight data points by ranking, cutoff, or custom selection.
   - Adjust text annotation properties and spacing between labels to avoid overlap.
4. **View and Export Figures**:
   - Interact with the figure on the dashboard, or download the static version created with Matplotlib.

## Project Structure

- **app.py**: Main application file for running the Dash app.
- **callbacks.py**: Handles app callbacks for interactivity and figure updates.
- **utils.py**: Utility functions for data processing and figure generation.
- **static_figure.png**: Default output path for saved static figures.

## Contributing

Contributions are welcome! If you'd like to suggest improvements, report issues, or submit a pull request, please visit the [GitHub repository](https://github.com/chaochungkuo/AnnoFig).