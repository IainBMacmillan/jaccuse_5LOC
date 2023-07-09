import time
import random
import sys
from game_data import game_cards, set_place_name_length, set_place_name_commands, control_data, set_zophie_clues

# Set up the constants:
SUSPECTS: list = ['DUKE HAUTDOG', 'MAXIMUM POWERS', 'BILL MONOPOLIS', 'SENATOR SCHMEAR', 'MRS. FEATHERTOSS',
                  'DR. JEAN SPLICER', 'RAFFLES THE CLOWN', 'ESPRESSA TOFFEEPOT', 'CECIL EDGAR VANDERTON']
ITEMS: list = ['FLASHLIGHT', 'CANDLESTICK', 'RAINBOW FLAG', 'HAMSTER WHEEL', 'ANIME VHS TAPE', 'JAR OF PICKLES',
               'ONE COWBOY BOOT', 'CLEAN UNDERPANTS', '5 DOLLAR GIFT CARD']
PLACES: list = ['ZOO', 'OLD BARN', 'DUCK POND', 'CITY HALL', 'HIPSTER CAFE', 'BOWLING ALLEY', 'VIDEO GAME MUSEUM',
                'UNIVERSITY LIBRARY', 'ALBINO ALLIGATOR PIT']

# Set up the constants:
TIME_TO_SOLVE: int = 300  # 300 seconds (5 minutes) to solve the game.
MAX_GUESSES: int = 3  # allowed to accuse before game ends

# First letters and longest length of places are needed for menu display:
PLACE_FIRST_LETTERS: dict = set_place_name_commands()
LONGEST_PLACE_NAME_LENGTH: int = set_place_name_length()
DECK: list = game_cards()
liars: list = control_data.get_liars()
culprit: str = control_data.get_culprit()

# Create data structures for clues the truth-tellers give about each item and suspect.
# clues: Keys=suspects being asked for a clue, value="clue dictionary".
clues: dict = {}
interviewee: str
for i, interviewee in enumerate(SUSPECTS):
    if interviewee in liars:
        continue  # Skip the liars for now.

    # This "clue dictionary" has keys=items & suspects, value=the clue given.
    clues[interviewee]: dict = {}
    clues[interviewee]['debug_liar'] = False  # Useful for debugging.
    item: str
    for item in ITEMS:  # Select clue about each item.
        if random.randint(0, 1) == 0:  # Tell where the item is:
            clues[interviewee][item] = PLACES[ITEMS.index(item)]
        else:  # Tell who has the item:
            clues[interviewee][item] = SUSPECTS[ITEMS.index(item)]
    suspect: str
    for suspect in SUSPECTS:  # Select clue about each suspect.
        if random.randint(0, 1) == 0:  # Tells where the suspect is:
            clues[interviewee][suspect] = PLACES[SUSPECTS.index(suspect)]
        else:  # Tells what item the suspect has:
            clues[interviewee][suspect] = ITEMS[SUSPECTS.index(suspect)]

# Create data structures for clues the liars give about each item and suspect:
for i, interviewee in enumerate(SUSPECTS):
    if interviewee not in liars:
        continue  # We've already handled the truth-tellers.

    # This "clue dictionary" has keys=items & suspects, value=the clue given:
    clues[interviewee]: dict = {}
    clues[interviewee]['debug_liar'] = True  # Useful for debugging.

    # This interviewee is a liar and gives wrong clues:
    for item in ITEMS:
        if random.randint(0, 1) == 0:
            while True:  # Select a random (wrong) place clue.
                # Lies about where the item is.
                clues[interviewee][item] = random.choice(PLACES)
                if clues[interviewee][item] != PLACES[ITEMS.index(item)]:
                    # Break out of the loop when wrong clue is selected.
                    break
        else:
            while True:  # Select a random (wrong) suspect clue.
                clues[interviewee][item] = random.choice(SUSPECTS)
                if clues[interviewee][item] != SUSPECTS[ITEMS.index(item)]:
                    # Break out of the loop when wrong clue is selected.
                    break
    for suspect in SUSPECTS:
        if random.randint(0, 1) == 0:
            while True:  # Select a random (wrong) place clue.
                clues[interviewee][suspect] = random.choice(PLACES)
                if clues[interviewee][suspect] != PLACES[SUSPECTS.index(suspect)]:
                    # Break out of the loop when wrong clue is selected.
                    break
        else:
            while True:
                # Select a random (wrong) item clue.
                clues[interviewee][suspect] = random.choice(ITEMS)
                if clues[interviewee][suspect] != ITEMS[SUSPECTS.index(suspect)]:
                    # Break out of the loop when wrong clue is selected.
                    break


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

knownSuspectsAndItems: list = []
# visitedPlaces: Keys=places, values=strings of the suspect & item there.
visitedPlaces: dict = {}
currentLocation: str = 'TAXI'  # Start the game at the taxi.
accusedSuspects: list = []  # Accused suspects won't offer clues.
accusationsLeft: int = MAX_GUESSES  # You can accuse up to 3 people.

startTime: float = time.time()
endTime: float = startTime + TIME_TO_SOLVE

while True:  # Main game loop.
    if time.time() > endTime or accusationsLeft == 0:
        # Handle "game over" condition:
        if time.time() > endTime:
            print('You have run out of time!')
        elif accusationsLeft == 0:
            print('You have accused too many innocent people!')
            culpritIndex = SUSPECTS.index(culprit)
            print('It was {} at the {} with the {} who catnapped her!'.format(culprit, PLACES[culpritIndex],
                                                                              ITEMS[culpritIndex]))
            print('Better luck next time, Detective.')
            sys.exit()

    print()
    minutesLeft: int = int(endTime - time.time()) // 60
    secondsLeft: int = int(endTime - time.time()) % 60
    print('Time left: {} min, {} sec'.format(minutesLeft, secondsLeft))

    if currentLocation == 'TAXI':
        print(' You are in your TAXI. Where do you want to go?')
        for place in sorted(visitedPlaces):
            placeInfo: str = visitedPlaces[place]
            nameLabel: str = '(' + place[0] + ')' + place[1:]
            spacing: str = " " * (LONGEST_PLACE_NAME_LENGTH - len(place))
            print('{} {}{}'.format(nameLabel, spacing, placeInfo))
        print('(Q)UIT GAME')
        while True:  # Keep asking until a valid response is given.
            response = input('> ').upper()
            if response == '':
                continue  # Ask again.
            if response == 'Q':
                print('Thanks for playing!')
                sys.exit()
            if response in PLACE_FIRST_LETTERS.keys():
                currentLocation = PLACE_FIRST_LETTERS[response]
                break

        continue  # Go back to the start of the main game loop.

    # At a place; player can ask for clues.
    print(' You are at the {}.'.format(currentLocation))
    currentLocationIndex: int = PLACES.index(currentLocation)
    thePersonHere: str = SUSPECTS[currentLocationIndex]
    theItemHere: str = ITEMS[currentLocationIndex]
    print(' {} with the {} is here.'.format(thePersonHere, theItemHere))

    # Add the suspect and item at this place to our list of known suspects and items:
    if thePersonHere not in knownSuspectsAndItems:
        knownSuspectsAndItems.append(thePersonHere)
    if ITEMS[currentLocationIndex] not in knownSuspectsAndItems:
        knownSuspectsAndItems.append(ITEMS[currentLocationIndex])
    if currentLocation not in visitedPlaces.keys():
        visitedPlaces[currentLocation] = '({}, {})'.format(thePersonHere.lower(), theItemHere.lower())

    # If the player has accused this person wrongly before, they won't give clues:
    if thePersonHere in accusedSuspects:
        print('They are offended that you accused them,')
        print('and will not help with your investigation.')
        print('You go back to your TAXI.')
        print()
        input('Press Enter to continue...')
        currentLocation = 'TAXI'
        continue  # Go back to the start of the main game loop.

    # Display menu of known suspects & items to ask about:
    print()
    print('(J) "J\'ACCUSE!" ({} accusations left)'.format(accusationsLeft))
    print('(Z) Ask if they know where ZOPHIE THE CAT is.')
    print('(T) Go back to the TAXI.')
    for i, suspectOrItem in enumerate(knownSuspectsAndItems):
        print('({}) Ask about {}'.format(i + 1, suspectOrItem))

    while True:  # Keep asking until a valid response is given.
        response = input('> ').upper()
        if response == '':
            continue  # Ask again.
        if response in 'JZT' or (response.isdecimal() and 0 < int(response) <= len(knownSuspectsAndItems)):
            break

    if response == 'J':  # Player accuses this suspect.
        accusationsLeft -= 1  # Use up an accusation.
        if thePersonHere == culprit:
            # You've accused the correct suspect.
            print('You\'ve cracked the case, Detective!')
            print('It was {} who had catnapped ZOPHIE THE CAT.'.format(culprit))
            minutesTaken = int(time.time() - startTime) // 60
            secondsTaken = int(time.time() - startTime) % 60
            print('Good job! You solved it in {} min, {} sec.'.format(minutesTaken, secondsTaken))
            sys.exit()
        else:
            # You've accused the wrong suspect.
            accusedSuspects.append(thePersonHere)
            print('You have accused the wrong person, Detective!')
            print('They will not help you with anymore clues.')
            print('You go back to your TAXI.')
            currentLocation = 'TAXI'

    elif response == 'Z':  # Player asks about Zophie.
        zophieClues: dict = set_zophie_clues()
        if thePersonHere not in zophieClues:
            print('"I don\'t know anything about ZOPHIE THE CAT."')
        elif thePersonHere in zophieClues:
            print(' They give you this clue: "{}"'.format(zophieClues[thePersonHere]))
            # Add non-place clues to the list of known things:
            if zophieClues[thePersonHere] not in knownSuspectsAndItems and \
               zophieClues[thePersonHere] not in PLACES:
                knownSuspectsAndItems.append(zophieClues[thePersonHere])

    elif response == 'T':  # Player goes back to the taxi.
        currentLocation = 'TAXI'
        continue  # Go back to the start of the main game loop.

    else:  # Player asks about a suspect or item.
        thingBeingAskedAbout = knownSuspectsAndItems[int(response) - 1]
        if thingBeingAskedAbout in (thePersonHere, theItemHere):
            print(' They give you this clue: "No comment."')
        else:
            print(' They give you this clue: "{}"'.format(clues[thePersonHere][thingBeingAskedAbout]))
            # Add non-place clues to the list of known things:
            if clues[thePersonHere][thingBeingAskedAbout] not in knownSuspectsAndItems and \
               clues[thePersonHere][thingBeingAskedAbout] not in PLACES:
                knownSuspectsAndItems.append(clues[thePersonHere][thingBeingAskedAbout])

    input('Press Enter to continue...')
