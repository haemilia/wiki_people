# 으라차차~ 위키키킼! - Wikipedia 기반 유명인 인생사 시각화
# Visualization of Famous People's Biographies Based on Wikipedia
## Description
- Biographical Visualization based on Wikipedia articles of [various famous people](https://www.biographyonline.net/people/famous-twentieth-century.html). 
- Used AllenNLP's **Coreference Resolution** and spaCy's **POS-tagging** to extract relevant life events with mentions of a specific year.
- Used OpenAI API to divide life events into either Career / Personal Life event.
- Each person's life is visualized using Plotly and Dash. Summary visualizations made using Tableau are also available.
## Dependencies
- Due to AllenNLP's Coreference Resolution process being unstable, it is recommended to use separate environments for analysis and visualization.
- Analysis dependencies are not guaranteed to be supported. 
- Use conda environments for easy use.
```bash
conda env create -f PATH/TO/DEPENDENCIES.yaml -p PATH/TO/YOUR/CONDA/ENVIRONMENTS/your_env_name
```
## Visualization Demo
You must install the [dependencies for the visualization](visualization\dependencies_visualization.yaml), and activate the environment. Then, in the command prompt, do the following commands:
1. Run `visualization_app.py`
```bash
python visualization/visualization_app.py
```
2. It will ask for the root directory of the repository. Please input the root directory path.
```bash
Please input root directory: REPOSITORY/ROOT/DIRECTORY/PATH
```
3. If successful, it will show something like this. Click on the http link to access the visualization for individual graphs and the link for the Tableau visualization.
```bash
Dash is running on http://CLICK/ON/LINK/HERE/

 * Serving Flask app 'visualization_app'
 * Debug mode: on
```

Made for YBIGTA DA Together Project 2023-2.