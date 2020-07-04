from Deck import Deck
from Player import Bot, RealPlayer, Dealer
from consts import MESSAGES
import random
import time


class Game:

    def __init__(self):
        self.deck = Deck()
        self.bots = []
        self.total_players = []
        self.not_stand_players = []
        self.starting_player_money = 200
        self.min_bet, self.max_bet = 1, 20
        self.max_bots_allowable = 6
        self.player, self.dealer = RealPlayer(self.starting_player_money), Dealer()

    def start_game(self):

        while True:
            start_game = input(MESSAGES['Starting?'])
            if start_game.lower() == 'n':
                exit()
            elif start_game.lower() == 'y':
                print(MESSAGES['Game rules'])
                break

        while True:
            number_of_bots = input(MESSAGES['Bots number'])
            if number_of_bots.isdigit() and int(number_of_bots) <= self.max_bots_allowable:
                break
            else:
                print(MESSAGES['Bots warning'])

        self._create_bots(number_of_bots)

    def play_game(self):

        # shuffle deck
        random.shuffle(self.deck.cards)

        # ask for a bet
        self._ask_for_bet(self.player)

        # deal first two cards
        self._deal_first_two_cards()

        # deal cards until everyone is not standing
        while len(self.not_stand_players) > 0:
            self._deal_third_and_further_cards(self.not_stand_players)

        # open dealer cards and take more if needed
        while not self.dealer.stand:
            self._deal_third_and_further_cards([self.dealer])

        # print all cards before end of the game
        self._current_open_cards()

    def end_game(self):
        self._calculate_game_results()
        self._print_game_results()
        self._get_cards_from_players()
        self._ask_continue_to_play()

    def _deal_first_two_cards(self):
        for player in self.total_players * 2:
            new_card = self.deck.give_card()
            player.add_card(new_card)
        self._update_not_stand_players()

    def _update_not_stand_players(self):
        self.not_stand_players = [player for player in self.total_players
                                  if not player.type == 'Dealer' and not player.stand]

    def _deal_third_and_further_cards(self, players_list):
        for player in players_list:
            while not player.stand:
                if player.type != 'Real Player':
                    new_card = self.deck.give_card()
                    player.add_card(new_card)
                elif player.type == 'Real Player' and self._ask_player_for_new_card(player):
                    new_card = self.deck.give_card()
                    player.add_card(new_card)
        self._update_not_stand_players()

    def _ask_player_for_new_card(self, player):
        self._current_open_cards()
        print(f'Dealer has {self.dealer.visible_card().points} points')
        choice = input(f'You have {player.type_of_points} {player.points}. Wanna hit or stand?(h/s) ')
        if choice.lower() == 'h':
            return True
        elif choice.lower() == 's':
            player.stand = True
            return False

    def _current_open_cards(self):
        if len(self.not_stand_players) > 0:
            for player in self.total_players:
                if player.type == 'Dealer':
                    player.print_one_card()
                else:
                    player.print_cards()
        else:
            for player in self.total_players:
                player.print_cards()

    def _create_bots(self, number_of_bots):
        for i in range(1, int(number_of_bots) + 1):
            new_bot = Bot()
            self.bots.append(new_bot)

        self._update_total_players_list()

    def _update_total_players_list(self):
        self.total_players.append(self.player)
        self.total_players += self.bots
        random.shuffle(self.total_players)
        self.total_players.insert(0, self.dealer)

    def _ask_for_bet(self, player):
        while True:
            user_input_bet = input(f'You have {player.money_available} dollars. ' +
                                   f'How much do you wanna bet? (from {self.min_bet} to {self.max_bet}) ')
            if user_input_bet.isdigit() and player.money_available < int(user_input_bet):
                print(MESSAGES['No money'])
            elif user_input_bet.isdigit() and self.min_bet <= int(user_input_bet) <= self.max_bet:
                break
            else:
                print(MESSAGES['Bet warning'])
        player.current_bet = int(user_input_bet)

    def _print_game_results(self):
        dealer_points = self.dealer.points
        print('\n' + 'Game Results'.center(70, '-') + '\n' + 'Player: ' + self.dealer.type.ljust(15) +
              'Total points: ' + str(dealer_points) + '\n')

        for player in [players for players in self.total_players if players.type != 'Dealer']:
            print('Player: ' + player.type.ljust(15) + 'Total points: ' + str(player.points).ljust(15) +
                  'Result: ' + player.game_result.ljust(15))

        self._print_player_result(self.player)

    def _calculate_game_results(self):
        dealer_points = self.dealer.points

        for player in [players for players in self.total_players if players.type != 'Dealer']:
            if player.points == 21 and player.number_of_cards() == 2:
                player.game_result = 'BlackJack'
            elif player.points > 21:
                player.game_result = 'Loss'
            else:
                if player.points > dealer_points or dealer_points > 21:
                    player.game_result = 'Win'
                elif player.points < dealer_points:
                    player.game_result = 'Loss'
                else:
                    player.game_result = 'Draw'

    def _print_player_result(self, player):
        print('\nYour result: ', end='')
        if player.game_result == 'Win':
            player.money_available += player.current_bet
            print(f'You have won {player.current_bet}! You have {player.money_available} dollars now.')
        elif player.game_result == 'Loss':
            player.money_available -= player.current_bet
            print(f'You have lost {player.current_bet} :( You have {player.money_available} dollars now.')
        elif player.game_result == 'BlackJack' and (self.dealer.number_of_cards != 2 or self.dealer.points != 21):
            money_won = round(player.current_bet * 1.5)
            player.money_available += money_won
            print('Hurray! You have got a BlackJack' +
                  f'You have won {money_won}! You have {player.money_available} dollars now.')
        else:
            print(f'It is a draw! You still have {player.money_available} dollars.')

    def _ask_continue_to_play(self):
        if self.player.money_available < 1:
            print(MESSAGES['No money to continue'])
            time.sleep(3)
            exit()

        while True:
            start_game = input('Another round? (y/n) ')
            if start_game.lower() == 'n':
                print(f'\nYour final result: {self.player.money_available - 200}')
                time.sleep(5)
                exit()
            elif start_game.lower() == 'y':
                break
        self.deck = Deck()
        self.play_game()
        self.end_game()

    def _get_cards_from_players(self):
        for player in self.total_players:
            player.reset_player_data()


