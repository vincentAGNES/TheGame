from game_utils import read_file, \
    write_file, \
    get_list_disabled, \
    get_player_to_play, \
    get_message, \
    is_game_over, \
    generate_player_cards, \
    generate_boards_card


import os
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

class Player:
    def __init__(self, number):

        self.name = "player" + str(number)
        self.number = number
        self.cards_file = "./data/hand_" + str(number) + '.txt'
        if not os.path.exists(self.cards_file):
            with open(self.cards_file, 'w') as f:
                f.write("none")
        self.header = dbc.Row(
                [
                    dbc.Col(dbc.Button(id=self.name + "_next_button", children="Fin du tour", color="success", className="mr-1", disabled=True)),
                    dbc.Col(dbc.Progress(id=self.name + "_progress", value=0, animated=True), style={"margin-top": '15px'}),
                    dbc.Col(dbc.Alert(id=self.name + "_alert", children="", color="warning")),

                ],
                className="mb-4",
                style={'margin-left': '5px', 'margin-right': '5px', 'margin-top':'5px'}
            )

        self.cards_board = dbc.Row(
                [
                    dbc.Col(dbc.Card(id=self.name + '_board_1', children=generate_boards_card(1), color="warning", inverse=True)),
                    dbc.Col(dbc.Card(id=self.name + '_board_2', children=generate_boards_card(1), color="warning", inverse=True)),
                    dbc.Col(dbc.Card(id=self.name + '_board_3', children=generate_boards_card(100, decreasing=True), color="info", inverse=True)),
                    dbc.Col(dbc.Card(id=self.name + '_board_4', children=generate_boards_card(100, decreasing=True), color="info", inverse=True)),
                ],
                className="mb-3",
                style={'margin-left': '5px', 'margin-right': '5px', 'margin-top':'5px'}
            )


        self.cards_player = dbc.Row(
                [
                    dbc.Col(dbc.Card(generate_player_cards(None, 1, player=self.name), id=self.name +'_card_player_1', color="secondary", inverse=True)),
                    dbc.Col(dbc.Card(generate_player_cards(None, 2, player=self.name), id=self.name +'_card_player_2', color="secondary", inverse=True)),
                    dbc.Col(dbc.Card(generate_player_cards(None, 3, player=self.name), id=self.name +'_card_player_3', color="secondary", inverse=True)),
                    dbc.Col(dbc.Card(generate_player_cards(None, 4, player=self.name), id=self.name +'_card_player_4', color="secondary", inverse=True)),
                    dbc.Col(dbc.Card(generate_player_cards(None, 5, player=self.name), id=self.name +'_card_player_5', color="secondary", inverse=True)),
                    dbc.Col(dbc.Card(generate_player_cards(None, 6, player=self.name), id=self.name +'_card_player_6', color="secondary", inverse=True)),
                ],
                className="mb-4",
                style={'margin-left': '5px', 'margin-right': '5px', 'margin-top':'5px', 'margin-bottom':'5px'}
            )

        self.layout = html.Div([self.header, self.cards_board, self.cards_player])

        self.outputList = [Output(self.name + "_card_player_{}".format(i), "children") for i in range(1,7)] +\
            [Output(self.name + "_board_{}".format(i), "children") for i in range(1,5)] +\
            [Output(self.name + '_next_button', 'disabled'),
                Output(self.name + '_alert', 'children'),
                Output(self.name + '_progress', 'value')
            ]

        self.inputList = [Input(self.name + '_next_button', 'n_clicks')] +\
            [Input(self.name + "_btn_{}_{}".format(i, j), "n_clicks") for i in range(1, 7) for j in range(1, 5)] +\
            [Input("interval-component", 'n_intervals')]

        self.stateList = State(self.name + '_next_button', 'disabled')

    def callback_func(self, ctx, next_button_state=False, dir='data'):

        hand_file = self.cards_file
        if not ctx.triggered:
            button_id = 'No click yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        hand = read_file(hand_file)
        table = read_file(os.path.join(dir,'table.json'))
        players = read_file(os.path.join(dir,"players.json"))

        if button_id == self.name + "_next_button":
            cartes = read_file(os.path.join(dir,"cartes.txt"))
            picked_carte = cartes[:hand.count(999)]
            write_file(os.path.join(dir,"cartes.txt"), cartes[hand.count(999):])
            if len(cartes[hand.count(999):]) == 0:  # tas de cartes finis
                write_file(os.path.join(dir,"state.txt"), 'final')
            hand = list(filter(lambda a: a != 999, hand))
            hand = hand + picked_carte
            if len(hand) < 6:  # tas de carte finis
                for i in range(6 - len(hand)):
                    hand = hand + [999]
            hand.sort()
            write_file(hand_file, hand)
            disabled_next_button = True
            write_file(os.path.join(dir,'player.txt'), players[str(self.number)])

        elif button_id == 'No click yet' or button_id == 'interval-component':
            disabled_next_button = next_button_state

        else:
            sp = button_id.split('_')
            keys = ["1_1", "1_2", "100_1", "100_2"]
            key = keys[int(sp[3]) - 1]
            table[key] = hand[int(sp[2]) - 1]
            write_file(os.path.join(dir,'table.json'), table)
            hand[int(sp[2]) - 1] = 999
            write_file(hand_file, hand)
            state = read_file(os.path.join(dir,'state.txt'))
            hist = read_file(os.path.join(dir,'historic.txt'))
            disabled_next_button = not (hist == self.number or \
                                        state == 'final' or \
                                        hand.count(999) == 6)
            write_file(os.path.join(dir,'historic.txt'), self.number)

        if sum([sum(get_list_disabled(hand[i], table, self.number)) for i in range(6)]) == 0 \
                and get_player_to_play() == self.number \
                and hand.count(999) != 6 \
                and disabled_next_button:
            write_file(os.path.join(dir,"state.txt"), 'over')

        if is_game_over():
            write_file(os.path.join(dir,"state.txt"), 'win')

        alert_content = get_message(read_file(os.path.join(dir,'state.txt')), self.number, dir)

        cartes = read_file(os.path.join(dir,"cartes.txt"))
        progress_value = 100 - len(cartes)
        return [
            generate_player_cards(hand[0], 1, get_list_disabled(hand[0], table, self.number), player=self.name),
            generate_player_cards(hand[1], 2, get_list_disabled(hand[1], table, self.number), player=self.name),
            generate_player_cards(hand[2], 3, get_list_disabled(hand[2], table, self.number), player=self.name),
            generate_player_cards(hand[3], 4, get_list_disabled(hand[3], table, self.number), player=self.name),
            generate_player_cards(hand[4], 5, get_list_disabled(hand[4], table, self.number), player=self.name),
            generate_player_cards(hand[5], 6, get_list_disabled(hand[5], table, self.number), player=self.name),
            generate_boards_card(table["1_1"]),
            generate_boards_card(table["1_2"]),
            generate_boards_card(table["100_1"], decreasing=True),
            generate_boards_card(table["100_2"], decreasing=True),
            disabled_next_button,
            alert_content,
            progress_value
        ]


