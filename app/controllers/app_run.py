import dash
from dash import html, callback
from dash.dependencies import Input, Output
import os, sys

# Get the path to the directory containing the 'app' package
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(app_dir)

from app_route_callbacks import display_page_callback

external_stylesheets = ["./static/dashboard_stylesheet.css", "./static/forms_stylesheet.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    [dash.dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    return display_page_callback(pathname)



if __name__ == "__main__":
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=True)
