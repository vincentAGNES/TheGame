import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import os
from utils import read_file, write_file

update_interval = dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )

def generate_player_cards(N, pos, L_disabled=[1 for i in range(4)], player=''):
    buttons = dbc.ButtonGroup(
        [dbc.Button(str(i), id= player + "_btn_{}_{}".format(pos,i), color="info", outline=L_disabled[i-1]==0, disabled=L_disabled[i-1]==0) for i in range(1,5)],
        size="sm"
    )
    if N == 999:
        card_content = [
            dbc.CardHeader(),
            dbc.CardBody(buttons, style={"visibility": "hidden"}),
        ]
    else:
        card_content = [
            dbc.CardHeader("Carte numéro {}".format(N), style={"text-align": "center"}),
            dbc.CardBody(
                [
                    html.H1(str(N)),
                    buttons,
                    html.Div([dbc.Tooltip("Placer sur le tas " + str(i), target=player + "_btn_{}_{}".format(pos, i), placement='bottom') for i in range(1, 5)])
                ], style={"text-align": "center"}
            ),
        ]
    return card_content


def generate_boards_card(N, decreasing=False):
    card_content = [
        dbc.CardHeader("1 → 100" if not decreasing else "100 → 1", style={"text-align": "center"}),
        dbc.CardBody([html.H1(str(N), style={"text-align": "center"}),])
    ]

    return card_content




def get_player_to_play(dir='data'):
    with open(os.path.join(dir,"player.txt"), 'r') as f:
        try:
            player_to_play = int(f.read())
        except:
            player_to_play = int(f.read().split()[-1])
    # Check if player is done
    hand = read_file(os.path.join(dir,"hand_{}.txt".format(player_to_play)))
    if hand.count(999)==6:
        players = read_file(os.path.join(dir,"players.json"))
        write_file(os.path.join(dir, 'player.txt'), players[str(player_to_play)])
        return players[str(player_to_play)]
    return player_to_play



def get_list_disabled(hand_val, table, player):
    player_to_play = get_player_to_play()
    L_disabled = [1 for i in range(4)]
    if hand_val == 999 or player_to_play != player:
        return [0 for i in range(4)]
    if hand_val > table["1_1"] or table["1_1"] - hand_val == 10:
        L_disabled[0] = 1
    else:
        L_disabled[0] = 0
    if hand_val > table["1_2"] or table["1_2"] - hand_val == 10:
        L_disabled[1] = 1
    else:
        L_disabled[1] = 0
    if hand_val < table["100_1"] or table["100_1"] - hand_val == -10:
        L_disabled[2] = 1
    else:
        L_disabled[2] = 0
    if hand_val < table["100_2"] or table["100_2"] - hand_val == -10:
        L_disabled[3] = 1
    else:
        L_disabled[3] = 0
    return L_disabled

def get_message(state, player, dir):
    game = read_file(os.path.join(dir, 'game.json'))

    if state == 'win':
        alert_content = dcc.Markdown('''C'est gagné, **Félicitations !!!**''')
    elif state =='over':
        alert_content = dcc.Markdown('''C'est perdu, **Vous êtes mauvais !!!**''')
    elif player == get_player_to_play():
        alert_content = dcc.Markdown("**A toi de jouer ! ** _Oublie pas d'appuyer sur fin du tour_")
    else:
        alert_content = dcc.Markdown('''En attente de **{}**'''.format(game["players_name"][str(get_player_to_play())]))
    return alert_content


def is_game_over(dir='data'):
    state = read_file(os.path.join(dir, 'state.txt'))
    bool = [False for i in range(1,7)]
    for i in range(1,7):
        hand = read_file(os.path.join(os.path.join(dir,'hand_{}.txt'.format(i))))
        if len(hand)==0 or hand.count(999) == 6: # player_i is done
            bool[i-1] = True
    if state == 'final' and sum(bool)==6:
        return True
    else:
        return False