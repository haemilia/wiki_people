import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly
import plotly.graph_objs as go
import pandas as pd
from pathlib import Path
import os


HOME_PATH = Path(r"C:\Users\lhi30\Haein\2023\YBIGTA\2023-2\DA\Wiki_People\Share")
def get_visualization_data(relative_path = "data/final_df/", labeled = True) -> dict:
    """
    From the input path, return a dictionary od pandas DataFrames, with the csv files' names as the keys

    Parameters:
    - relative_path (str): The relative path of the folder with all the csv files ready for visualization

    Returns:
    - df_dict[name] = df: A dictionary with name(str) as the key, and the DataFrame as the value
    """
    if labeled:
        relative_path = "data/labeled_final_df/"
        get_path = HOME_PATH / relative_path
        csv_list = os.listdir(get_path)
        df_dict = {}
        for csv_file in csv_list:
            name = csv_file[:-12]
            df = pd.read_csv(HOME_PATH / relative_path / csv_file)
            df_dict[name] = df
        return df_dict
    else:
        get_path = HOME_PATH / relative_path
        csv_list = os.listdir(get_path)
        df_dict = {}
        for csv_file in csv_list:
            name = csv_file[:-4]
            df = pd.read_csv(HOME_PATH / relative_path / csv_file)
            df_dict[name] = df
        return df_dict

def generate_timeline(person_name: str, person_df: pd.DataFrame) -> plotly.graph_objects.Figure:
    """
    Generate a life timeline plot for a person based on the provided DataFrame.

    Parameters:
    - person_name (str): The name of the person.
    - person_df (pd.DataFrame): DataFrame containing ["year", "age", "event", "category1", "category2", "Personal Life / Career"].

    Returns:
    - plotly.graph_objects.Figure: The generated timeline plot.
    """

    def generate_hover_text(row: pd.DataFrame):
        hover_text = row["event"]
        if pd.notna(row["category1"]):
            hover_text += f"<br><b>Heading:</b> {row['category1']}"
        if pd.notna(row["category2"]):
            hover_text += f"<br><b>Sub-Heading:</b> {row['category2']}"

        hover_text +=f"<br><b>Category:</b> {row['Career/Personal Life']}"
        return hover_text

    # Given the information we have, let's generate what to display
    person_df["hover_text"] = person_df.apply(generate_hover_text, axis=1)

    # Define colors based on "Personal Life / Career" column
    color_dict = {"Personal Life": "gold", "Career": "skyblue"}
    person_df["marker_color"] = person_df["Career/Personal Life"].map(color_dict)

    # Let's create the plot's title
    figure_title = f"{person_name}'s Life, according to Wikipedia"

    # The actual graph figure!
    fig = go.Figure()

    # Add the data points with different colors
    for category, category_df in person_df.groupby("Career/Personal Life"):
        fig.add_trace(
            go.Scatter(
                x=category_df["year"],
                y=[1] * len(category_df),
                mode="markers+text",
                marker=dict(size=20, color=color_dict[category]),
                text=category_df["year"].astype(str) + " - Age: " + category_df["age"].astype(str),
                hoverinfo="text",
                hovertext=category_df["hover_text"],
                showlegend=False,
                textposition="bottom center",
                textfont=dict(color="black", size=10, family="inherit"),
            )
        )

    fig.update_layout(
        title=figure_title,
        xaxis=dict(showgrid=True, showline=True, showticklabels=True, ticks="outside"),
        yaxis=dict(showgrid=False, showline=False, showticklabels=False),
        hovermode="closest",
    )

    return fig


app = dash.Dash(__name__)

# Tableau link
tableau_link = 'https://public.tableau.com/views/urachacha_wikikikik_final/1_1?:language=en-US&:display_count=n&:origin=viz_share_link'

df_dict = get_visualization_data()
name_figures = {}
for name, df in df_dict.items():
    figure = generate_timeline(name, df)
    name_figures[name] = figure

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='name-dropdown',
            options=[
                {'label': name, 'value': name} for name in name_figures.keys()
            ],
            value=list(name_figures.keys())[0],
            style={'width': '50%', 'margin-bottom': '20px'}
        ),

        html.Div(id='selected-name-figure-placeholder', style={'width': '100%'})
    ], style={'width': '100%', 'margin-bottom': '20px'}),

    html.Div([
        # Replace the initial figure with the Tableau link
        html.A(
            "Open Tableau Visualization",
            href=tableau_link,
            target='_blank',
            style={'display': 'block', 'text-align': 'center', 'font-weight': 'bold', 'font-size': '20px'}
        )
    ], style={'width': '100%'}),
])

@app.callback(
    Output('selected-name-figure-placeholder', 'children'),
    [Input('name-dropdown', 'value')]
)
def display_selected_name_figure(selected_name):
    if selected_name:
        selected_figure = name_figures.get(selected_name, name_figures[list(name_figures.keys())[0]])
        return dcc.Graph(
            id='selected-name-figure',
            figure=selected_figure,
            style={'width': '100%'}
        )
    return None

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
