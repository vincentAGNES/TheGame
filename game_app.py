import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from game_utils import update_interval
from player import Player

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
server = app.server

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

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'), Input('url', 'href')])
def display_page(pathname, href):
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
        L = [dcc.Markdown('''Va voir ces liens:''')]
        for i in range(1, 7):
            href_ = "{}player{}".format(href, i)
            L = L + [dcc.Markdown('''{}'''.format(href_))]
        return L


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
    app.run_server(debug=True, port=9001, host='0.0.0.0')
    #app.run_server(debug=True, , port=9001)
