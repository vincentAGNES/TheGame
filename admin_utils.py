import random
import json
import os
from TheGame.utils import read_file, write_file

def pick_cards(N, dir="data"):
    cartes = read_file(os.path.join(dir,'cartes.txt'))
    picked_carte = cartes[:N]
    write_file(os.path.join(dir,'cartes.txt'), cartes[N:])
    return picked_carte


def preprocess(n_player, vals, dir='data'):
    game = {}
    game['n_player'] = n_player
    game['players_name'] = {}
    if not os.path.exists(dir):
        os.mkdir(dir)
    for en, val in enumerate(vals):
        if val is not None:
            game['players_name'][str(en + 1)] = val
    with open(os.path.join(dir, 'game.json'), 'w') as f:
        json.dump(game, f)

    # create deck
    cartes = list(range(2,100))
    random.shuffle(cartes)
    with open(os.path.join(dir, 'cartes.txt'), 'w') as f:
        for i in cartes:
            f.write('{}\n'.format(i))

    # initiate table
    table = {"100_1": 100, "100_2": 100, "1_1": 1, "1_2": 1}
    with open(os.path.join(dir, 'table.json'), 'w') as f:
        json.dump(table, f)

    # creating a json to give next player
    players = {str(i): str((i + 1) % (n_player+1) + (i + 1) // (n_player+1)) for i in range(1, n_player+1)}
    with open(os.path.join(dir, 'players.json'), 'w') as f:
        json.dump(players, f)

    # distribuer les cartes
    for player_ in range(1, 7):
        with open(os.path.join(dir, 'hand_{}.txt'.format(player_)), 'w') as f:
            if player_ <= n_player:
                picked_cards = pick_cards(6)
                for i in picked_cards:
                    f.write('{}\n'.format(i))
            else:
                f.write('none')

    # keep track of the actual player
    with open(os.path.join(dir,'player.txt'), 'w') as f:
        f.write('1')

    # keep track of the state
    with open(os.path.join(dir,'state.txt'), 'w') as f:
        f.write('playing')

    with open(os.path.join(dir,'historic.txt'), 'w') as fd:
        fd.write('0')
