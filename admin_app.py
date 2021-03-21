import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from admin_utils import preprocess

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
server = app.server

checklist = dbc.RadioItems(
    id="input_number_player",
    options=[
        {"label": "{} joueurs".format(i), "value": i} for i in range(2,7)
    ],
    labelCheckedStyle={"color": "red"},
)

app.layout = html.Div([
    html.H5(" Combien de joueurs ? "),
    checklist,
    html.H5(id='input_user', style=dict(margin="10px")),
    html.Div([dbc.Input(placeholder="Nom du joueur {}".format(i),
                       style={"display":"none"},
                       id="name_{}".format(i)) for i in range(1,7)]),
    dbc.Button("Lancer la partie", id="validation_button", color="info", className="mr-1", disabled=True, style={"display":"none"}),
    html.P(id="target"),
    dcc.Location(id='url', refresh=False)
], style={'margin':'10px'})


@app.callback([Output("input_user","children"), Output("validation_button","style")] + \
    [Output("name_{}".format(i), "style") for i in range(1,7)],
    [Input('input_number_player', 'value')])
def index_callback(val):
    hidden = {"display":"none"}
    visible = {"margin-top":"2px", "display":"block"}
    if val is not None:
        return ["Entrez le nom de chaque joueur:", visible] + [visible if i<=val else hidden for i in range(1,7)]
    else:
        return ["", hidden] + [hidden for i in range(1,7)]

@app.callback(Output("target", "children"),
              [Input("validation_button", "n_clicks"), Input('url', 'href')],
              [State('input_number_player', 'value')] + [State("name_{}".format(i), 'value') for i in range(1,7)])
def index_callback(n_click, href_input,  n_player, *vals):

    if n_click is not None:
        preprocess(n_player, vals, dir='./data')
        L=[dcc.Markdown('''Envoi ces liens à tes coéquipiers:''')]
        for i in range(1,n_player+1):
            href = "{}9001/player{}".format(href_input.split('9000')[0], i)
            L = L + [dcc.Markdown('''{} : {}'''.format(vals[i], href))]
        return L
    else:
        preprocess(6, vals, dir='./data')
        return None

@app.callback(Output("validation_button","disabled"),
              [Input('input_number_player', 'value')]+[Input("name_{}".format(i), 'value') for i in range(1,7)])
def index_callback(number_player, *vals):
    if number_player is not None:
        if vals.count(None) == 6-number_player:
            return False
    return True

#if __name__ == '__main__':
    #app.run_server(debug=True, port=9000)
    #app.run_server(debug=True, port=9000, host='0.0.0.0')
