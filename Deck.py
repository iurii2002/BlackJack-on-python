from consts import SUITS, RANKS


class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.points = self._calculate_card_point()

    def _calculate_card_point(self):
        if self.rank == 'A':
            points = 11
        elif self.rank.isdigit():
            points = int(self.rank)
        else:
            points = 10
        return points

    def __str__(self):
        message = 'Card: ' + self.rank + ' of ' + self.suit + ' ||| ' + 'Points: ' + str(self.points)
        return message


class Deck:

    def __init__(self):
        self.cards = self._create_52_cards()

    @staticmethod
    def _create_52_cards():
        cards = []
        for suit, rank in ((suit, rank) for suit in SUITS for rank in RANKS):
            card = Card(rank, suit)
            cards.append(card)
        return cards

    def give_card(self):
        card = self.cards.pop(0)
        return card

    def __len__(self):
        return len(self.cards)
