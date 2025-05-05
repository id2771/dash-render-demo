# app.py
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# 1) Charge les données
df = pd.read_csv("athlete_events.csv")

# 2) Crée l'app Dash
app = Dash(__name__)
server = app.server   # nécessaire pour gunicorn

# 3) Layout : dropdown pays, slider année, graphique
app.layout = html.Div([
    html.H1("Tableau de bord JO"),
    dcc.Dropdown(
        id="pays",
        options=[{"label": r, "value": r} for r in sorted(df.region.dropna().unique())],
        value="United States",
        clearable=False,
    ),
    dcc.Slider(
        id="annee",
        min=int(df.Year.min()),
        max=int(df.Year.max()),
        value=int(df.Year.max()),
        marks={y: str(y) for y in range(int(df.Year.min()), int(df.Year.max())+1, 20)},
        step=None,
    ),
    dcc.Graph(id="bar-chart")
])

# 4) Callback : met à jour le graphique
@app.callback(
    Output("bar-chart", "figure"),
    Input("pays", "value"),
    Input("annee", "value"),
)
def update_chart(pays, annee):
    dfi = df[(df.region == pays) & (df.Year == annee)]
    top10 = dfi.Sport.value_counts().nlargest(10)
    fig = px.bar(
        x=top10.index,
        y=top10.values,
        labels={"x": "Sport", "y": "Nombre d'athlètes"},
        title=f"Top 10 sports – {pays} – {annee}"
    )
    return fig

# 5) Lancement local
if __name__ == "__main__":
    app.run_server(debug=True)
