from time import time
from game_data import SuspectProfiles, GameData

suspect_profiles: SuspectProfiles = SuspectProfiles()
game_data: GameData = GameData(suspect_profiles)

# Set up the constants:
SUSPECTS: list = suspect_profiles.suspects
ITEMS: list = suspect_profiles.items
PLACES: list = suspect_profiles.places
TIME_TO_SOLVE: int = 300  # 300 seconds (5 minutes) to solve the game.
MAX_GUESSES: int = 3  # allowed to accuse before game ends

# First letters and longest length of places are needed for menu display:
DIRECTION_COMMANDS: dict = game_data.direction_commands
CLUE_COMMANDS: dict = {'J': '"J\'ACCUSE!"',
                       'Z': 'Ask if they know where ZOPHIE THE CAT is',
                       'T': 'Go back to the TAXI.'}
LONGEST_PLACE_NAME_LENGTH: int = game_data.place_name_length
culprit: str = suspect_profiles.culprit
# clues = set_suspect_clues()
clues: dict = game_data.suspect_clues
# zophie_clues = set_zophie_clues()
zophie_clues: dict = game_data.zophie_clues


def user_input(valid_commands: dict) -> str:
    user_response: str = ''
    responded: bool = False
    while not responded:
        user_response: str = input('> ').upper()
        if user_response == '':
            continue
        if user_response in str(valid_commands.keys()):
            responded = True
    return user_response


def update_known_clues(clue: str) -> None:
    clues_count: int = len(CLUE_COMMANDS) - 2
    if clue not in CLUE_COMMANDS.values():
        print(f'{len(CLUE_COMMANDS)} : {clues_count} : {clue} : ')
        CLUE_COMMANDS[clues_count] = clue


def update_visited_places(visited_places: dict, place: str, person: str, item: str) -> None:
    if place not in visited_places.keys():
        visited_places[place] = '({}, {})'.format(person.lower(), item.lower())


def play_jaccuse() -> None:
    # START OF THE GAME
    print("""J'ACCUSE! (a mystery game)
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

    # visitedPlaces: Keys=places, values=strings of the suspect & item there.
    visited_places: dict = {}
    ask_direction: str = 'TAXI'  # Start the game at the taxi.
    accused_suspects: list = []  # Accused suspects won't offer clues.
    accusations_left: int = MAX_GUESSES  # You can accuse up to 3 people.

    start_time: float = time()
    end_time: float = start_time + TIME_TO_SOLVE
    game_over: bool = False
    while not game_over:  # Main game loop.
        if time() > end_time == 0:
            game_over = True
            print('You have run out of time!')
            continue
        print()
        minutes_left: int = int(end_time - time()) // 60
        seconds_left: int = int(end_time - time()) % 60
        print('Time left: {} min, {} sec'.format(minutes_left, seconds_left))

        # get_directions
        if ask_direction == 'TAXI':
            # presentation
            print(' You are in your TAXI. Where do you want to go?')
            for place in sorted(visited_places):
                name_label: str = '(' + place[0] + ')' + place[1:]
                spacing: str = " " * (LONGEST_PLACE_NAME_LENGTH - len(place))
                place_info: str = visited_places[place]
                print('{} {}{}'.format(name_label, spacing, place_info))
            print('(Q)UIT GAME')
            # user input
            ask_command: str = user_input(DIRECTION_COMMANDS)
            ask_direction: str = DIRECTION_COMMANDS[ask_command]
            # game_update
            if ask_direction == 'QUIT GAME':
                game_over = True
            continue  # Go back to the start of the main game loop.

        # At a place; player can ask for clues.
        # update game
        current_location_index: int = PLACES.index(ask_direction)
        the_person_here: str = SUSPECTS[current_location_index]
        the_item_here: str = ITEMS[current_location_index]
        update_known_clues(the_person_here)
        update_known_clues(the_item_here)
        update_visited_places(visited_places=visited_places,
                              place=ask_direction, person=the_person_here, item=the_item_here)
        # presentation
        print(' You are at the {}.'.format(ask_direction))
        print(' {} with the {} is here.'.format(the_person_here, the_item_here))

        # If the player has accused this person wrongly before, they won't give clues:
        if the_person_here in accused_suspects:
            print('They are offended that you accused them,')
            print('and will not help with your investigation.')
            print('You go back to your TAXI.')
            print()
            input('Press Enter to continue...')
            ask_direction = 'TAXI'
            continue  # Go back to the start of the main game loop.

        # Display menu of known suspects & items to ask about:
        print()
        for key in CLUE_COMMANDS:
            if key != 'J':
                print(f'({key}) {CLUE_COMMANDS[key]}')
            else:
                print(f'({key}) {CLUE_COMMANDS[key]} ({accusations_left}) accusations left')

        clue_selected: str = user_input(CLUE_COMMANDS)

        if clue_selected == 'J':  # Player accuses this suspect.
            accusations_left -= 1  # Use up an accusation.
            if the_person_here == culprit:
                # You've accused the correct suspect.
                print('You\'ve cracked the case, Detective!')
                minutes_taken = int(time() - start_time) // 60
                seconds_taken = int(time() - start_time) % 60
                print('Good job! You solved it in {} min, {} sec.'.format(minutes_taken, seconds_taken))
                game_over = True
            else:
                # You've accused the wrong suspect.
                accused_suspects.append(the_person_here)
                print('You have accused the wrong person, Detective!')
                print('They will not help you with anymore clues.')
                print('You go back to your TAXI.')
                ask_direction = 'TAXI'
            if accusations_left == 0:
                print('You have accused too many innocent people!')
                game_over = True
                continue

        elif clue_selected == 'Z':  # Player asks about Zophie.
            zophie_clue_answers: dict = game_data.zophie_clues  # set_zophie_clues()
            if the_person_here not in zophie_clue_answers:
                print('"I don\'t know anything about ZOPHIE THE CAT."')
            elif the_person_here in zophie_clue_answers:
                print(' They give you this clue: "{}"'.format(zophie_clue_answers[the_person_here]))
                # Add non-place clues to the list of known things:
                if zophie_clue_answers[the_person_here] not in CLUE_COMMANDS.values() and \
                        zophie_clue_answers[the_person_here] not in PLACES:
                    update_known_clues(the_person_here)

        elif clue_selected == 'T':  # Player goes back to the taxi.
            ask_direction = 'TAXI'

        else:  # Player asks about a suspect or item.
            thing_being_asked_about = CLUE_COMMANDS[int(clue_selected)]
            if thing_being_asked_about in (the_person_here, the_item_here):
                print(' They give you this clue: "No comment."')
            else:
                system_response: str = clues[the_person_here][thing_being_asked_about]
                print(' They give you this clue: "{}"'.format(system_response))
                # Add non-place clues to the list of known things:
                if system_response not in CLUE_COMMANDS.values() and \
                        system_response not in PLACES:
                    update_known_clues(system_response)

        input('Press Enter to continue...')


def main() -> None:
    play_jaccuse()
    print('\n\nThank you for playing.\n\n')
    culprit_index = SUSPECTS.index(culprit)
    print('It was {} at the {} with the {} who catnapped her!'.format(culprit, PLACES[culprit_index],
                                                                      ITEMS[culprit_index]))
    print('Better luck next time, Detective.')


if __name__ == '__main__':
    main()
