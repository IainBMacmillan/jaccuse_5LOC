from dataclasses import dataclass
from random import shuffle, choice, randint, sample
from functools import reduce
from enum import Enum


# Set up the constants:
SUSPECTS: list = ['DUKE HAUTDOG', 'MAXIMUM POWERS', 'BILL MONOPOLIS', 'SENATOR SCHMEAR', 'MRS. FEATHERTOSS',
                  'DR. JEAN SPLICER', 'RAFFLES THE CLOWN', 'ESPRESSA TOFFEEPOT', 'CECIL EDGAR VANDERTON']
ITEMS: list = ['FLASHLIGHT', 'CANDLESTICK', 'RAINBOW FLAG', 'HAMSTER WHEEL', 'ANIME VHS TAPE', 'JAR OF PICKLES',
               'ONE COWBOY BOOT', 'CLEAN UNDERPANTS', '5 DOLLAR GIFT CARD']
PLACES: list = ['ZOO', 'OLD BARN', 'DUCK POND', 'CITY HALL', 'HIPSTER CAFE', 'BOWLING ALLEY', 'VIDEO GAME MUSEUM',
                'UNIVERSITY LIBRARY', 'ALBINO ALLIGATOR PIT']


shuffle(SUSPECTS)
shuffle(PLACES)
shuffle(ITEMS)


@dataclass
class SetupData:
    liars: list
    culprit: str

    def __init__(self, table: list):
        self.liars = sample(table, randint(3, 4))
        self.culprit = choice(table)

    def get_liars(self) -> list:
        return self.liars

    def get_culprit(self) -> str:
        return self.culprit


control_data = SetupData(SUSPECTS)
LIARS: list = control_data.get_liars()
CULPRIT: str = control_data.get_culprit()


class KindOfClue(Enum):
    PLACE = 1
    SUSPECT = 2
    ITEM = 3


def game_cards() -> list:
    deck: list = []
    for i, place in enumerate(PLACES):
        card: dict = {PLACES[i]: [SUSPECTS[i], ITEMS[i]]}
        deck.append(card)
    return deck


def get_card_from_deck(location: str, deck: list) -> dict:
    card: dict
    for card in deck:
        for key in card:
            if key == location:
                return card


def set_place_name_length() -> int:
    res: str = reduce(lambda x, y: x if len(x) > len(y) else y, PLACES)
    longest_place_name_length: int = len(res)
    return longest_place_name_length


def set_place_name_commands() -> dict:  # First letters and longest length of places are needed for menu display:
    place_first_letters: dict = {}
    place: str
    for place in PLACES:
        place_first_letters[place[0]] = place
    return place_first_letters


def identify_zophie_clues(interviewee: str, liars: list, culprit: str, table: list) -> str:
    response: str
    culprit_index: int = SUSPECTS.index(culprit)
    if interviewee not in liars:  # They tell you who has Zophie.
        response = table[culprit_index]
    else:
        liar_index = randint(0, 8)
        while liar_index == culprit_index:
            liar_index = randint(0, 8)
        else:
            response = table[liar_index]
    return response


def set_zophie_clues() -> dict:
    # a subset of suspects know who has Zophie. This method creates the clues
    # based on :
    zophie_clues: dict = {}
    zophie_know_alls: list = sample(SUSPECTS, randint(3, 4))
    liars: list = LIARS
    culprit: str = CULPRIT

    for interviewee in zophie_know_alls:
        kind_of_clue: int = randint(1, 3)
        if kind_of_clue == KindOfClue.PLACE.value:
            zophie_clues[interviewee] = identify_zophie_clues(interviewee=interviewee, liars=liars,
                                                              culprit=culprit, table=SUSPECTS)
        elif kind_of_clue == KindOfClue.SUSPECT.value:
            zophie_clues[interviewee] = identify_zophie_clues(interviewee=interviewee, liars=liars,
                                                              culprit=culprit, table=PLACES)
        elif kind_of_clue == KindOfClue.ITEM.value:
            zophie_clues[interviewee] = identify_zophie_clues(interviewee=interviewee, liars=liars,
                                                              culprit=culprit, table=ITEMS)
    return zophie_clues


def main() -> None:
    # ladds: dict = set_place_name_commands()
    # print(ladds)

    # max_place_length: int = set_place_name_length()
    # print(max_place_length)

    # deck: list = game_cards()
    # card: dict = get_card_from_deck(location=choice(PLACES), deck=deck)
    # print(card)

    # zophie_clues: dict = set_zophie_clues()
    # print(zophie_clues)
    pass


if __name__ == '__main__':
    main()
