import sys

import controllers, models


tournaments = []
players = []


def _list_choices_and_execute(function_mapping):
    while True:
        for i, (choice, _, *args) in enumerate(function_mapping):
            print(f'{i}: {choice}')
        selection = input('Select a choice: ')

        try:
            selection = int(selection)
            function = function_mapping[selection][1]
            args = function_mapping[selection][2:]
            break
        except ValueError:
            print('Selection must be an integer')
        except IndexError:
            print('Index out of range, try again')
    if function is None:
        print('Sorry that feature has not been implemented yet.')
    else:
        function(*args)


def main_menu():
    function_mapping = [
        ('Add tournament', add_tournament),
        ('View tournaments', view_tournaments),
        ('Add player', add_player),
        ('View players', view_players),
        ('Generate reports', None),
        ('exit', sys.exit),
    ]

    _list_choices_and_execute(function_mapping)


def add_tournament():
    tournament = controllers.create_model(models.Tournament)
    tournaments.append(tournament.to_dict())
    main_menu()


def add_player():
    player = controllers.create_model(models.Player)
    players.append(player.to_dict())
    main_menu()


def view_tournaments():
    function_mapping = [
        (tournament['name'], view_tournament, i) for i, tournament in enumerate(tournaments)
    ]
    if function_mapping:
        _list_choices_and_execute(function_mapping)
    else:
        print('No tournaments to display\n')
        main_menu()


def view_tournament(i):
    tournament = tournaments[i]
    print(f'Tournament {tournament["name"]}')
    function_mapping = [
        ('Start New Round', None),
        ('View Rounds', None),
        ('View Matches', None),
        ('View Players', view_tournament_players, i),
        ('Add Players', add_players_to_tournament, i),
        ('Edit Tournament', None),
        ('Delete Tournament', None),
        ('Back to Main Menu', main_menu),
    ]
    _list_choices_and_execute(function_mapping)


def add_players_to_tournament(tournament_index):
    for i, player in enumerate(players):
        print(f'{i}: {player["first_name"]} {player["last_name"]}')

    while True:
        players_list = input(
            'Please enter the players you would like to add as a list eg. [0, 3, 4. 5]')
        tournament = tournaments[tournament_index]
        tournament_players = tournament['players']
        try:
            players_list = list(players_list)
            players_list = [int(i) for i in players_list]
        except ValueError:
            print('Incorrect input. Try again:')
            continue

        for i in players_list:
            try:
                player = players[i]
                if i in tournament_players:
                    print(f'{player["first_name"]} {player["last_name"]} is already added, skipping...')
                else:
                    tournament_players.append(i)
            except IndexError:
                print(f'Player {i} does not exist. skipping...')
        break
    tournament['players'] = tournament_players
    view_tournament(tournament_index)


def _view_players(function, *args, players_list=players):
    function_mapping = [
        (f'{player["first_name"]} {player["last_name"]}', function, player_index, *args)
        for player_index, player in enumerate(players)
    ]
    if function_mapping:
        _list_choices_and_execute(function_mapping)
    else:
        print('No Players to display\n')
        main_menu()


def view_players():
    _view_players(view_player)


def view_tournament_players(tournament_index):
    tournament = tournaments[tournament_index]
    _view_players(view_tournament_player, tournament_index, players_list=tournament['players'])


def view_player(i):
    player = players[i]
    print(f'Player: {player["first_name"]} {player["last_name"]}')
    function_mapping = [
        ('View Matches', None),
        ('Edit Player', None),
        ('Delete Player', None),
        ('Back to Main Menu', main_menu),
    ]
    _list_choices_and_execute(function_mapping)


def view_tournament_player(player_index, tournament_index):
    function_mapping = [
        ('View Matches', None),
        ('Remove from tournament', None),
        ('Back to Main Menu', main_menu),
    ]
    _list_choices_and_execute(function_mapping)
