from dataclasses import dataclass
from random import shuffle, choice, randint, sample
from functools import reduce
from enum import Enum
# from reverse_engineering import show_clues


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
class SuspectProfiles:
    # create the suspects characters
    places: list
    suspects: list
    items: list
    zophie_know_alls: list
    liars: list
    culprit: str

    def __init__(self):
        self.places = PLACES
        self.suspects = SUSPECTS
        self.items = ITEMS
        self.liars = sample(SUSPECTS, randint(3, 4))
        self.zophie_know_alls = sample(SUSPECTS, randint(3, 4))
        self.culprit = choice(SUSPECTS)


def set_suspect_clues(liars: list) -> dict:
    # Create data structures for clues the truth-tellers give about each item and suspect.
    # clues: Keys=suspects being asked for a clue, value="clue dictionary".
    clues: dict = {}
    witness: str
    for i, witness in enumerate(SUSPECTS):
        if witness in liars:
            continue  # Skip the liars for now.

        # This "clue dictionary" has keys=items & suspects, value=the clue given.
        clues[witness]: dict = {}
        item: str
        for item in ITEMS:  # Select clue about each item.
            table: list = choice([PLACES, SUSPECTS])
            clues[witness][item] = table[ITEMS.index(item)]

        suspect: str
        for suspect in SUSPECTS:  # Select clue about each suspect.
            table: list = choice([PLACES, ITEMS])
            clues[witness][suspect] = table[SUSPECTS.index(suspect)]

    # Create data structures for clues the liars give about each item and suspect:
    for i, witness in enumerate(SUSPECTS):
        if witness not in liars:
            continue  # We've already handled the truth-tellers.

        # This "clue dictionary" has keys=items & suspects, value=the clue given:
        clues[witness]: dict = {}

        # This witness is a liar and gives wrong clues:
        for item in ITEMS:
            table: list = choice([PLACES, SUSPECTS])
            response: str = choice(table)
            while response == table[ITEMS.index(item)]:
                response = choice(table)
            clues[witness][item] = response

        for suspect in SUSPECTS:
            table: list = choice([PLACES, ITEMS])
            response: str = choice(table)
            while response == table[SUSPECTS.index(suspect)]:
                response = choice(table)
            clues[witness][suspect] = response
    return clues


def get_zophie_clue(witness: str, table: list, suspect_profiles: SuspectProfiles) -> str:
    response: str
    culprit_index: int = suspect_profiles.suspects.index(suspect_profiles.culprit)
    # liar_index: int = -1  # needed to ensure randint works properly
    if witness not in suspect_profiles.liars:  # They tell you who has Zophie.
        response = table[culprit_index]
    else:
        liar_index: int = randint(0, 8)
        while liar_index == culprit_index:
            liar_index = randint(0, 8)
        response = table[liar_index]
    return response


def set_zophie_clues(suspect_profiles: SuspectProfiles) -> dict:
    # a subset of suspects know who has Zophie. This method creates the clues
    # based on :
    zophie_clues: dict = {}
    zophie_know_alls: list = suspect_profiles.zophie_know_alls

    for witness in zophie_know_alls:
        kind_of_clue: int = randint(1, 3)
        if kind_of_clue == KindOfClue.PLACE.value:
            zophie_clues[witness] = get_zophie_clue(witness=witness,
                                                    table=SUSPECTS, suspect_profiles=suspect_profiles)
        elif kind_of_clue == KindOfClue.SUSPECT.value:
            zophie_clues[witness] = get_zophie_clue(witness=witness,
                                                    table=PLACES, suspect_profiles=suspect_profiles)
        elif kind_of_clue == KindOfClue.ITEM.value:
            zophie_clues[witness] = get_zophie_clue(witness=witness,
                                                    table=ITEMS, suspect_profiles=suspect_profiles)
    return zophie_clues


@dataclass
class GameData:
    witness_clues: dict
    zophie_clues: dict
    direction_commands: dict
    place_name_length: int

    def __init__(self, suspect_profiles: SuspectProfiles):
        self.witness_clues = set_suspect_clues(liars=suspect_profiles.liars)
        self.zophie_clues = set_zophie_clues(suspect_profiles=suspect_profiles)
        self.direction_commands = set_direction_commands()
        self.place_name_length = set_place_name_length()


class KindOfClue(Enum):
    PLACE = 1
    SUSPECT = 2
    ITEM = 3


def set_place_name_length() -> int:
    res: str = reduce(lambda x, y: x if len(x) > len(y) else y, PLACES)
    longest_place_name_length: int = len(res)
    return longest_place_name_length


def set_direction_commands() -> dict:  # First letters and longest length of places are needed for menu display:
    place_first_letters: dict = {}
    place: str
    for place in PLACES:
        place_first_letters[place[0]] = place
    place_first_letters['Q'] = 'QUIT GAME'
    return place_first_letters


def main() -> None:
    suspect_profiles = SuspectProfiles()
    game_data = GameData(suspect_profiles)
    # ladds: dict = set_direction_commands()
    # print(ladds)

    # max_place_length: int = set_place_name_length()
    # print(max_place_length)

    zophie_clues: dict = game_data.zophie_clues
    print(zophie_clues)

    # clues: dict = game_data.witness_clues
    # for clue in clues:
    #     print(f'Clue: {clue}')

    # suspect_answers: dict = set_suspect_clues(liars=suspect_profiles.liars)
    # show_clues(clues=suspect_answers, suspects=SUSPECTS)
    pass


if __name__ == '__main__':
    main()