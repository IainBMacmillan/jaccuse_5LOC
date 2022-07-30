import sys
import time
import random
from enum import Enum

# Set up the constants:
SUSPECTS: list[str] = ['DUKE HAUTDOG', 'MAXIMUM POWERS', 'BILL MONOPOLIS', 'SENATOR SCHMEAR', 'MRS. FEATHERTOSS',
                       'DR. JEAN SPLICER', 'RAFFLES THE CLOWN', 'ESPRESSA TOFFEEPOT', 'CECIL EDGAR VANDERTON']
ITEMS: list[str] = ['FLASHLIGHT', 'CANDLESTICK', 'RAINBOW FLAG', 'HAMSTER WHEEL', 'ANIME VHS TAPE', 'JAR OF PICKLES',
                    'ONE COWBOY BOOT', 'CLEAN UNDERPANTS', '5 DOLLAR GIFT CARD']
PLACES: list[str] = ['ZOO', 'OLD BARN', 'DUCK POND', 'CITY HALL', 'HIPSTER CAFE', 'BOWLING ALLEY', 'VIDEO GAME MUSEUM',
                     'UNIVERSITY LIBRARY', 'ALBINO ALLIGATOR PIT']
TIME_TO_SOLVE: int = 300  # 300 seconds (5 minutes) to solve the game.
GUESSES_J_ACCUSE = 3

# First letters and longest length of places are needed for menu display:
TAXI_DESTINATIONS: dict = {place[0]: place for place in PLACES}
LONGEST_PLACE_NAME_LENGTH: int = max(len(place) for place in PLACES)

# Common indexes link these; e.g. SUSPECTS[0] and ITEMS[0] are at PLACES[0].
random.shuffle(SUSPECTS)
random.shuffle(ITEMS)
random.shuffle(PLACES)

liars: list[str] = random.sample(SUSPECTS, random.randint(3, 4))
culprit: str = random.choice(SUSPECTS)

known_suspects_and_items: list[str] = []
# visitedPlaces: Keys=places, values=strings of the suspect & item there.
visited_places: dict[str, list[str]] = {}
accused_suspects: list[str] = []  # Accused suspects won't offer clues.


class Detective(Enum):
    travels = 1
    questions = 2
    gameover = 3


class Gameclock:

    def __init__(self) -> None:
        self._start_time = time.time()
        self._end_time = self._start_time + TIME_TO_SOLVE

    def display_remaining(self) -> None:
        minutes_left = int(self._end_time - time.time()) // 60
        seconds_left = int(self._end_time - time.time()) % 60
        print(f'\nTime left: {minutes_left} min, {seconds_left} sec')

    def display_used(self) -> None:
        minutes_used = int(time.time() - self._start_time) // 60
        seconds_used = int(time.time() - self._start_time) % 60
        print(f'\nTime Used: {minutes_used} min, {seconds_used} sec')

    def isover(self) -> bool:
        if self._end_time < time.time():
            return True
        return False


def identify_interviewee_clues() -> dict:
    def identify_truth_clues() -> dict:
        def identify_truth_clue(index: int, grouping: list) -> str:
            if random.randint(0, 1) == 0:  # Tell where the item is:
                clue = PLACES[index]
            else:  # Tell who has the item:
                clue = grouping[index]
            return clue

        clues = {}
        for interviewee in SUSPECTS:
            if interviewee in liars:
                continue  # Skip the liars for now.

            # This "clue dictionary" has keys=items & suspects, value=the clue given.
            clues[interviewee]: dict = {}
            clues[interviewee]['debug_liar'] = False  # Useful for debugging.

            for item in ITEMS:  # Select clue about each item.
                clues[interviewee][item] = identify_truth_clue(ITEMS.index(item), SUSPECTS)

            for suspect in SUSPECTS:  # Select clue about each item.
                clues[interviewee][suspect] = identify_truth_clue(SUSPECTS.index(suspect), ITEMS)
                # clues[interviewee][suspect] = truth_clue_from_suspect(suspect)

        return clues

    def identify_liar_clues() -> dict:
        def identify_liar_clue(index: int, grouping: list) -> str:
            if random.randint(0, 1) == 0:
                while True:  # Select a random (wrong) place clue.
                    clue = random.choice(PLACES)
                    if clue != PLACES[index]:
                        # Break out of the loop when wrong clue is selected.
                        break
            else:
                while True:
                    # Select a random (wrong) item clue.
                    clue = random.choice(grouping)
                    if clue != grouping[index]:
                        # Break out of the loop when wrong clue is selected.
                        break
            return clue

        clues: dict = {}
        for interviewee in liars:
            # This "clue dictionary" has keys=items & suspects, value=the clue given:
            clues[interviewee]: dict = {}
            clues[interviewee]['debug_liar'] = True  # Useful for debugging.

            # This interviewee is a liar and gives wrong clues:
            for item in ITEMS:
                clues[interviewee][item] = identify_liar_clue(ITEMS.index(item), SUSPECTS)
            for suspect in SUSPECTS:
                clues[interviewee][suspect] = identify_liar_clue(SUSPECTS.index(suspect), ITEMS)
        return clues

    # clues: Keys=suspects being asked for a clue, value="clue dictionary".
    clues: dict = {}
    clues.update(identify_truth_clues())
    clues.update(identify_liar_clues())
    return clues


def identify_zophie_clues() -> dict:
    # Create the data structures for clues given when asked about Zophie:
    zophie_clues = {}
    randomsuspects = random.sample(SUSPECTS, random.randint(3, 4))
    def identify_zophie_clue(index: int, grouping: list) -> str:
        clue: str = ''
        if interviewee not in liars:  # They tell you who has Zophie.
            clue = grouping[index]
        elif interviewee in liars:
            while True:  # Select a (wrong) suspect clue.
                clue = random.choice(grouping)
                if clue != culprit:
                    # Break out of the loop when wrong clue is selected.
                    break
        return clue

    for interviewee in randomsuspects:
        kind_of_clue = random.randint(1, 3)
        if kind_of_clue == 1:  # from SUSPECTS
            zophie_clues[interviewee] = identify_zophie_clue(SUSPECTS.index(culprit), SUSPECTS)
        elif kind_of_clue == 2:  # from PLACES
            zophie_clues[interviewee] = identify_zophie_clue(SUSPECTS.index(culprit), PLACES)
        elif kind_of_clue == 3:  # from ITEMS
            zophie_clues[interviewee] = identify_zophie_clue(SUSPECTS.index(culprit), ITEMS)

    return zophie_clues


def if_game_over(isover: bool, accusations: int) -> Detective:
    if isover or accusations == 0:
        if isover:
            print('You have run out of time!')
        else:
            print(f'You have accused too many innocent people!')
            culprit_index = SUSPECTS.index(culprit)
            print(f'It was {culprit} at the {PLACES[culprit_index]} with the {ITEMS[culprit_index]} who catnapped her!')
            print(f'Better luck next time, Detective.')
        return Detective.gameover


def jaccuse() -> None:

    accusations_left = GUESSES_J_ACCUSE  # You can accuse up to 3 people.
    detective_action: Detective = Detective.travels
    current_location = 'TAXI'  # Start the game at the taxi.

    clues = identify_interviewee_clues()
    zophie_clues = identify_zophie_clues()

    # START OF THE GAME
    print("""J'ACCUSE! (a mystery game)")
    By Al Sweigart al@inventwithpython.com 
    Inspired by Homestar Runner\'s "Where\'s an Egg?" game 
    
    You are the world-famous detective, Mathilde Camus. 
    ZOPHIE THE CAT has gone missing, and you must sift through the clues. 
    Suspects either always tell lies, or always tell the truth. Ask them 
    about other people, places, and items to see if the details they give are 
    truthful and consistent with your observations. Then you will know if 
    their clue about ZOPHIE THE CAT is true or not. Will you find ZOPHIE THE 
    CAT in time and accuse the guilty party? 
    """)
    input('Press Enter to begin...')

    clock = Gameclock()
    while True:  # Main game loop.
        if_game_over(clock.isover(), accusations_left)
        clock.display_remaining()

        if detective_action == Detective.gameover:
            # out of time, used all guesses, user quits
            sys.exit()

        elif detective_action == Detective.travels:
            print(' You are in your TAXI. Where do you want to go?')
            for place in sorted(visited_places):
                location_label = '(' + place[0] + ')' + place[1:]
                print(f'{location_label}')
            print('(Q)UIT GAME')

            current_location = TAXI_DESTINATIONS[ask_directions()]
            detective_action = Detective.questions
            # continue  # Go back to the start of the main game loop.

        elif detective_action == Detective.questions:
            # At a place; player can ask for clues.
            print(f' You are at the {current_location}.')
            current_location_index = PLACES.index(current_location)
            the_person_here = SUSPECTS[current_location_index]
            the_item_here = ITEMS[current_location_index]
            print(f' {the_person_here} with the {the_item_here} is here.')

            # Add the suspect and item at this place to our list of known suspects and items:
            if the_person_here not in known_suspects_and_items:
                known_suspects_and_items.append(the_person_here)
            if the_item_here not in known_suspects_and_items:
                known_suspects_and_items.append(the_item_here)
            if current_location not in visited_places.keys():
                visited_places[current_location] = [the_person_here.lower(), the_item_here.lower()]

            # If the player has accused this person wrongly before, they won't give clues:
            if the_person_here in accused_suspects:
                prompt = f'\nThey are offended that you accused them \n' \
                         f'and will not help with your investigation.\n' \
                         f'You go back to your TAXI.\n\n'

                print(prompt)
                input('Press Enter to continue...')
                detective_action = Detective.travels

            # Display menu of known suspects & items to ask about:
            print()
            print(f'(J) "J\'ACCUSE!" ({accusations_left} accusations left)')
            print(f'(Z) Ask if they know where ZOPHIE THE CAT is.')
            print(f'(T) Go back to the TAXI.')
            for i, suspectOrItem in enumerate(known_suspects_and_items):
                print(f'({i + 1}) Ask about {suspectOrItem}')

            answer = askinterviewee(known_suspects_and_items)

            if answer == 'J':  # Player accuses this suspect.
                accusations_left -= 1  # Use up an accusation.
                detective_action = accused_answer(clock, the_person_here)

                input('Press Enter to continue...')
            elif answer == 'Z':  # Player asks about Zophie.
                whereiszophie(the_person_here, zophie_clues)
                input('Press Enter to continue...')
            elif answer == 'T':  # Player goes back to the taxi.
                detective_action = Detective.travels
            else:  # Player asks about a suspect or item.
                interviewee_response(clues, answer, the_item_here, the_person_here)
                input('Press Enter to continue...')



def print_visited_places(place):
    if place in sorted(visited_places):
        place_info = visited_places[place]
        location_label = '(' + place[0] + ')' + place[1:]
        spacing = " " * (LONGEST_PLACE_NAME_LENGTH - len(place))
        print(f'{location_label} {spacing}{place_info}')


def interviewee_response(clues, known_clue, the_item_here, the_person_here):
    thing_being_asked_about = known_suspects_and_items[int(known_clue) - 1]
    if thing_being_asked_about in (the_person_here, the_item_here):
        print(f' They give you this clue: "No comment."')
    else:
        print(f' They give you this clue: "{clues[the_person_here][thing_being_asked_about]}"')
        # Add non-place clues to the list of known things:
        if clues[the_person_here][thing_being_asked_about] not in known_suspects_and_items and \
                clues[the_person_here][thing_being_asked_about] not in PLACES:
            known_suspects_and_items.append(clues[the_person_here][thing_being_asked_about])


def whereiszophie(the_person_here, zophie_clues):
    if the_person_here not in zophie_clues:
        print(f'"I don\'t know anything about ZOPHIE THE CAT."')
    elif the_person_here in zophie_clues:
        print(f' They give you this clue: "{zophie_clues[the_person_here]}"')
        # Add non-place clues to the list of known things:
        if zophie_clues[the_person_here] not in known_suspects_and_items and \
                zophie_clues[the_person_here] not in PLACES:
            known_suspects_and_items.append(zophie_clues[the_person_here])


def accused_answer(clock: Gameclock, the_person_here: str) -> Detective:
    if the_person_here == culprit:
        # You've accused the correct suspect.
        print('You\'ve cracked the case, Detective!  Good job!')
        print(f'It was {culprit} who had catnapped ZOPHIE THE CAT.')
        clock.display_used()
        answer = Detective.gameover
    else:
        # You've accused the wrong suspect.
        accused_suspects.append(the_person_here)
        print(f'You have accused the wrong person, Detective!\n'
              f'They will not help you with anymore clues.\n'
              f'You go back to your TAXI.')
        answer = Detective.travels
    return answer

def askinterviewee(known_clues: list) -> str:
    while True:  # Keep asking until a valid known_clue is given.
        response = input('> ').upper()
        if response in 'JZT' or (response.isdecimal() and 0 < int(response) <= len(known_clues)):
            break
    return response


def ask_directions() -> str:
    while True:  # Keep asking until a valid known_clue is given.
        response = input('> ').upper()
        if response == 'Q':
            print('Thanks for playing!')
            sys.exit()      # TODO need to figure a way to cetnralise the exit routine
        if response in TAXI_DESTINATIONS.keys():
            break
    return response


def main() -> None:
    jaccuse()


if __name__ == "__main__":
    main()
