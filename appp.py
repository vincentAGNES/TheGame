import dash
import dash_html_components as html

app = dash.Dash()
app.config.suppress_callback_exceptions = True
server = app.server

app.layout = html.Div([
    html.Div("rrrr", id='page-content'),
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='0.0.0.0')
