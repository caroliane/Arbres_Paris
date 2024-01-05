import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Charger le DataFrame
df1 = pd.read_csv('df2.csv')  # Assurez-vous de remplacer 'votre_fichier.csv' par le nom réel de votre fichier

# Créer l'application Dash
app = dash.Dash(__name__)

# Layout de l'application
app.layout = html.Div([
    html.H1("Exploration des données d'arbres à Paris"),
    
    # Filtres pour le domaine et le stade de développement
    html.Label("Sélectionnez le domaine :"),
    dcc.Dropdown(
        id='domaine-dropdown',
        options=[{'label': domaine, 'value': domaine} for domaine in df1['DOMANIALITE'].unique()],
        value='DOMANIALITE'
    ),
    
    html.Label("Sélectionnez le stade de développement :"),
    dcc.Dropdown(
        id='stade-dropdown',
        options=[{'label': stade, 'value': stade} for stade in df1['STADE DE DEVELOPPEMENT'].unique()],
        value='STADE DE DEVELOPPEMENT'
    ),
    
    # Histogrammes
    dcc.Graph(id='histogram-circonference'),
    dcc.Graph(id='histogram-hauteur')
])

# Callback pour mettre à jour les histogrammes en fonction des filtres
@app.callback(
    [Output('histogram-circonference', 'figure'),
     Output('histogram-hauteur', 'figure')],
    [Input('domaine-dropdown', 'value'),
     Input('stade-dropdown', 'value')]
)
def update_histograms(selected_domaines, selected_stades):
    filtered_df = df1[(df1['DOMANIALITE'] == selected_domaines) & (df1['STADE DE DEVELOPPEMENT'] == selected_stades)]

    # Histogramme de circonférence
    fig_circonference = px.histogram(filtered_df, x='CIRCONFERENCE (cm)', title=f"Histogramme circonférence par {selected_domaines} - {selected_stades}")

    # Histogramme de hauteur
    fig_hauteur = px.histogram(filtered_df, x='HAUTEUR (m)', title=f"Histogramme hauteur par {selected_domaines} - {selected_stades}")

    return fig_circonference, fig_hauteur

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)