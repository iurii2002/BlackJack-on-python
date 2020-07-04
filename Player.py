import abc
import random


class AbstractPlayer(abc.ABC):

    def __init__(self):
        self._cards = []
        self.points = 0
        self.stand = False
        self.game_result = ''
        self.type_of_points = 'Hard'  # if player has an Ace his points are soft, else they are hard

    def add_card(self, card):
        self._cards.append(card)
        self._add_points(card)
        self._check_player_stand_after_new_card(card)

    def _add_points(self, card):
        self.points += card.points

    def _check_player_stand_after_new_card(self, card):
        if card.rank == 'A':
            self.type_of_points = 'Soft'

        if self.type != 'Real Player':
            if self.points >= self.max_points and self.type_of_points == 'Hard':
                self.stand = True
            elif self.points > 21 and self.type_of_points == 'Soft':
                self.points -= 10
                self.type_of_points = 'Hard'
            elif self.points > self.max_points and self.type_of_points == 'Soft':
                self.stand = True

        elif self.type == 'Real Player':
            if self.points > 21 and self.type_of_points == 'Hard':
                self.stand = True
            elif self.points > 21 and self.type_of_points == 'Soft':
                self.points -= 10
                self.type_of_points = 'Hard'

        if self.points == 21:
            self.stand = True

    def print_cards(self):
        message_cards = ''
        for card in self._cards:
            message_cards += card.__str__().ljust(40) + '|' + '\n'

        message = '\n' + ''.ljust(40, '-') + \
                  '\n' + ('Player: ' + self.type).ljust(40) + '|' + \
                  '\n' + message_cards + \
                  ('Total point: ' + str(self.points)).ljust(40) + '|' + \
                  '\n' + ''.ljust(40, '-')
        print(message)

    def number_of_cards(self):
        return len(self._cards)

    def reset_player_data(self):
        self._cards = []
        self.points = 0
        self.stand = False
        self.game_result = ''
        self.type_of_points = 'Hard'


class RealPlayer(AbstractPlayer):
    type = 'Real Player'

    def __init__(self, money_available):
        super().__init__()
        self.money_available = money_available
        self.current_bet = 0


class Bot(AbstractPlayer):
    type = 'Bot'

    def __init__(self):
        super().__init__()
        self.max_points = random.randint(16, 18)


class Dealer(AbstractPlayer):
    type = 'Dealer'
    max_points = 17

    def print_one_card(self):
        message_cards = 'Card: hidden card'.ljust(40) + '|' + '\n' + self.visible_card().__str__().ljust(40) + '\n'
        message = '\n' + ''.ljust(40, '-') + \
                  '\n' + ('Player: ' + self.type).ljust(40) + '|' + \
                  '\n' + message_cards + \
                  ('Total point: ' + (str(self._cards[1].points) + '+')).ljust(40) + '|' + \
                  '\n' + ''.ljust(40, '-')
        print(message)

    def visible_card(self):
        if self.number_of_cards() == 2:
            return self._cards[1]
        elif self.number_of_cards() > 2:
            return self._cards
