import dash
import os
from dash import html, page_container

app = dash.Dash(__name__, use_pages=True)

app.layout = html.Div([
    page_container  # This dynamically loads the selected page
])

if __name__ == "__main__":
    render_port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=render_port, debug=False)
