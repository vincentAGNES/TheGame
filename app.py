import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from game_utils import update_interval
from player import Player
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


player1 = Player(1)
player2 = Player(2)
player3 = Player(3)
player4 = Player(4)
player5 = Player(5)
player6 = Player(6)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    update_interval
])

index_layout = html.Div([
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


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    ctx = dash.callback_context

    print(    ctx.triggered[0]['prop_id'].split('.')[0] )


    if pathname == '/player1':
        return player1.layout
    elif pathname == '/player2':
        return player2.layout
    elif pathname == '/player3':
        return player3.layout
    elif pathname == '/player4':
        return player4.layout
    elif pathname == '/player5':
        return player5.layout
    elif pathname == '/player6':
        return player6.layout
    else:
        return index_layout

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
            href = "{}/player{}".format(href_input.split('5000')[0], i)
            L = L + [dcc.Markdown('''{} : {}'''.format(vals[i-1], href))]
        return L
    else:
        return None

@app.callback(Output("validation_button","disabled"),
              [Input('input_number_player', 'value')]+[Input("name_{}".format(i), 'value') for i in range(1,7)])
def index_callback(number_player, *vals):
    if number_player is not None:
        if vals.count(None) == 6-number_player:
            return False
    return True


@app.callback(player1.outputList, player1.inputList, player1.stateList
)
def callback(*btns):
    ctx = dash.callback_context
    return player1.callback_func(ctx, next_button_state=btns[-1])

@app.callback(player2.outputList, player2.inputList, player2.stateList
)
def callback(*btns):
    ctx = dash.callback_context
    return player2.callback_func(ctx, next_button_state=btns[-1])

@app.callback(player3.outputList, player3.inputList, player3.stateList
)
def callback(*btns):
    ctx = dash.callback_context
    return player3.callback_func(ctx, next_button_state=btns[-1])

@app.callback(player4.outputList, player4.inputList, player4.stateList
)
def callback(*btns):
    ctx = dash.callback_context
    return player4.callback_func(ctx, next_button_state=btns[-1])

@app.callback(player5.outputList, player5.inputList, player5.stateList
)
def callback(*btns):
    ctx = dash.callback_context
    return player5.callback_func(ctx, next_button_state=btns[-1])

@app.callback(player6.outputList, player6.inputList, player6.stateList
)
def callback(*btns):
    ctx = dash.callback_context
    return player6.callback_func(ctx, next_button_state=btns[-1])


if __name__ == '__main__':
    app.run_server(debug=True, port=9000)
    #app.run_server(debug=True, port=5000, host='0.0.0.0')