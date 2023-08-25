from __future__ import annotations
from abc import ABC, abstractmethod
from game_data import GameData, SuspectProfiles
from time import time

MAX_GUESSES = 3

suspect_profiles: SuspectProfiles = SuspectProfiles()
game_data: GameData = GameData(suspect_profiles)
clue_menu: dict = {'J': '"J\'ACCUSE!"',
                   'Z': 'Ask if they know where ZOPHIE THE CAT is',
                   'T': 'Go back to the TAXI.'}

start_time: float = time()


class Context:
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which refepresents the current
    state of the Context.
    """

    _state = None
    _continue: bool
    _visited_places: dict
    _location_card: list = []  # contains a list of place, suspect, and item

    _accusations_left: int
    _accused_suspects: list

    _selected_clue: str

    """
    A reference to the current state of the context.
    """

    def __init__(self, state) -> None:
        self.transition_to(state)
        self._continue = True
        self.set_location(["taxi", "detective", "notepad"])
        self._visited_places = {}
        self._accusations_left = MAX_GUESSES
        self._accused_suspects = []
        self._selected_clue = "empty"

    def transition_to(self, state: State):
        """
        The context allows changing the State Object at runtime.
        """
        # print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def get_current_state(self):
        print(f"Current State is: {type(self._state).__name__}")
        return type(self._state).__name__

    def is_continue(self) -> bool:
        return self._continue

    def stop_playing(self):
        self._continue = not self._continue

    def set_location(self, details: list):
        self._location_card = details

    def get_location(self):
        return self._location_card

    """
    Taxi methods
    """

    def update_visited_places(self, place: str, person: str, item: str) -> None:
        if place not in self._visited_places.keys():
            self._visited_places[place] = '({}, {})'.format(person.lower(), item.lower())

    def display_visited_places(self) -> None:
        print(' You are in your TAXI. Where do you want to go?')
        for place in sorted(self._visited_places):
            name_label: str = '(' + place[0] + ')' + place[1:]
            spacing: str = " " * (game_data.place_name_length - len(place))
            place_info: str = self._visited_places[place]
            print('{} {}{}'.format(name_label, spacing, place_info))
        print('(Q)UIT GAME')

    def was_accused(self, suspect) -> bool:
        if suspect not in self._accused_suspects:
            return False
        return True

    """
    Jaccuse State methods
    """
    def update_accusations(self, suspect: str) -> None:
        self._accusations_left -= 1
        self._accused_suspects.append(suspect)

    def is_accusation_left(self) -> bool:
        if self._accusations_left == 0:
            return False
        return True

    def get_accusations_left(self) -> int:
        return self._accusations_left

    """
    Interview State Methods
    """
    def update_selected_clue(self, clue) -> None:
        self._selected_clue = clue

    def get_clue(self) -> str:
        return self._selected_clue
    """
    The Context delegates part of its behaviour to the current State object.
    """

    def display(self):
        self._state.display()

    def user_input(self):
        self._state.user_input()

    def update(self):
        self._state.update_game()


class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a back reference to the Context object,
    associated to the State.  This back reference can be used by States to
    transition the Context to another State.
    """

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def display(self) -> None:
        pass

    @abstractmethod
    def user_input(self) -> None:
        pass

    @abstractmethod
    def update_game(self) -> None:
        pass


"""
Concrete States implement various behaviours, associated with a state of the
Context.
"""


class TaxiState(State):

    _current_place: str

    def display(self) -> None:
        self.context.display_visited_places()

    def user_input(self) -> None:
        self._current_place: str = game_data.direction_commands[user_input(game_data.direction_commands)]

    def update_game(self) -> None:
        if self._current_place == "QUIT GAME":
            self.context.transition_to(QuitGameState())
            return
        # picked a valid location
        current_location_index: int = suspect_profiles.places.index(self._current_place)
        current_suspect: str = suspect_profiles.suspects[current_location_index]
        current_item: str = suspect_profiles.items[current_location_index]
        # check if already accused the suspect
        if self.context.was_accused(current_suspect):
            self.context.transition_to(AccusedState())
            return
        self.context.set_location([self._current_place, current_suspect, current_item])
        self.context.update_visited_places(self._current_place, current_suspect, current_item)
        # used in display locations
        update_known_clues(current_suspect)
        update_known_clues(current_item)
        #  change state
        self.context.transition_to((LocationState()))


class QuitGameState(State):
    def display(self) -> None:
        print('\n\nThank you for playing.\n\n')
        culprit = suspect_profiles.culprit
        culprit_index = suspect_profiles.suspects.index(culprit)
        place = suspect_profiles.places[culprit_index]
        item = suspect_profiles.items[culprit_index]
        print('It was {} at the {} with the {} who catnapped her!'.format(culprit, place, item))
        print('Better luck next time, Detective.')

    def user_input(self) -> None:
        pass

    def update_game(self) -> None:
        self.context.stop_playing()


class LocationState(State):

    _selected_clue: str

    def __init__(self):
        self._selected_clue = "empty"

    def display(self) -> None:
        place, suspect, item = self.context.get_location()
        print('You are at the {}.'.format(place))
        print(' {} with the {} is here.'.format(suspect, item))
        # Display menu of known suspects & items to ask about:
        self._display_clue_menu()

    def user_input(self) -> None:
        self._selected_clue = user_input(clue_menu)

    def update_game(self) -> None:
        match self._selected_clue:
            case 'J':
                self.context.transition_to((JaccuseState()))
            case 'Z':
                self.context.transition_to((ZophieState()))
            case 'T':
                self.context.transition_to((TaxiState()))
            case _:  # assuming a number from clues
                self.context.update_selected_clue(self._selected_clue)
                self.context.transition_to((InterviewState()))

    def _display_clue_menu(self) -> None:
        print()
        for key in clue_menu:
            if key != 'J':
                print(f'({key}) {clue_menu[key]}')
            else:
                print(f'({key}) {clue_menu[key]} ({self.context.get_accusations_left()}) accusations left')


class JaccuseState(State):

    def display(self) -> None:
        place, suspect, item = self.context.get_location()
        if suspect == suspect_profiles.culprit:
            # You've accused the correct suspect.
            print('You\'ve cracked the case, Detective!')
            minutes_taken = int(time() - start_time) // 60
            seconds_taken = int(time() - start_time) % 60
            print('Good job! You solved it in {} min, {} sec.'.format(minutes_taken, seconds_taken))
        else:
            # You've accused the wrong suspect.
            print('You have accused the wrong person, Detective!')
            print('They will not help you with anymore clues.')
            print('You go back to your TAXI.')

        if not self.context.is_accusation_left():
            print('You have accused too many innocent people!')

    def user_input(self) -> None:
        pass

    def update_game(self) -> None:
        place, suspect, item = self.context.get_location()
        self.context.update_accusations(suspect)
        if suspect != suspect_profiles.culprit and \
                self.context.is_accusation_left():
            self.context.transition_to(TaxiState())
        else:
            self.context.transition_to(QuitGameState())


class ZophieState(State):

    def display(self) -> None:
        place, suspect, item = self.context.get_location()
        if suspect not in game_data.zophie_clues:
            print('"I don\'t know anything about ZOPHIE THE CAT."')
        else:
            print(' They give you this clue: "{}"'.format(game_data.zophie_clues[suspect]))

    def user_input(self) -> None:
        pass

    def update_game(self) -> None:
        # Add non-place clues to the list of known things:
        place, suspect, item = self.context.get_location()
        if suspect not in game_data.zophie_clues:
            pass
        else:
            if game_data.zophie_clues[suspect] not in clue_menu.values() and \
                    game_data.zophie_clues[suspect] not in suspect_profiles.places:
                update_known_clues(suspect)
        self.context.transition_to(LocationState())


class InterviewState(State):

    def display(self) -> None:
        clue_in_question = clue_menu[int(self.context.get_clue())]
        place, suspect, item = self.context.get_location()
        if clue_in_question in (suspect, item):
            print(' They give you this clue: "No comment."')
        else:
            response = game_data.witness_clues[suspect][clue_in_question]
            print(' They give you this clue: "{}"'.format(response))

    def user_input(self) -> None:
        pass

    def update_game(self) -> None:
        clue_in_question = clue_menu[int(self.context.get_clue())]
        place, suspect, item = self.context.get_location()
        if clue_in_question in (suspect, item):
            pass
        else:
            response = game_data.witness_clues[suspect][clue_in_question]
            if response not in clue_menu.values() and \
                    response not in suspect_profiles.places:
                update_known_clues(response)
        self.context.transition_to(LocationState())


class AccusedState(State):
    def display(self) -> None:
        print('They are offended that you accused them,')
        print('and will not help with your investigation.')
        print('You go back to your TAXI.')
        print()

    def user_input(self) -> None:
        input('Press Enter to continue...')

    def update_game(self) -> None:
        self.context.transition_to((TaxiState()))


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

    clues_count: int = len(clue_menu) - 2
    if clue not in clue_menu.values():
        # print(f'{len(clue_menu)} : {clues_count} : {clue} : ')
        clue_menu[clues_count] = clue


def main():
    playing = Context(TaxiState())
    while playing.is_continue():
        playing.display()
        playing.user_input()
        playing.update()


if __name__ == "__main__":
    main()
