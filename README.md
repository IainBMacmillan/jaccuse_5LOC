# Refactoring "JAccuse game" with "5 Lines of Code" by Christen Clausen
I chose this game to exercise the 5 Lines of Code (5LOC) rather than the book's use of Typescript, as I wanted to use Python as the platform language as this is my lnaguage of choice to learn programming.  I have found wwhile attempting the refactoring that there are problems using this game due to the __tight coupling__ of the data between the different stages of execution.  

# Problems encountered
There was no modules in the original game, and program length was about 290 lines of code.  So I left the CONSTANTS at top level of indent and moved all code into a new method named JAcusse() which I then called from a default main() method.  a few copying errors were fixed to enable the game to run.  
This was the start for the first part learnig __5LOC__. 
5 lines of Code is a condition of being able to understand what a method/function is executing. By removing code and placing it in its own method/function and providing a suitable name for the method, it improves readability of the program.

# Game Description
## The Constants 
SUSPECTS, ITEMS and PLACES, Length of Game and number of guesses of who has Zophie.
## The game set-up. 
* Shuffled pack of above to randomise their cross-reference between each other in lists.  
* Identified Culprit from SUSPECTS.  
* Identified 3 or 4 suspects who LIE. i.e. provide wrong information for clues.  
* Each suspect has one clue about each other suspect and their associated item. Contained in a dictionary of dictionaries.  
* Identified 3 or 4 suspects that has clues about __Zophie the Cat__.  
* start and end time for game clock.
## Execution data
* Keep a record of places visited and suspects interviewed.  This is used to display where detective has been and who and what was there.
* Keep a record of clues and ordered by when Detective hears about them. This is used to display clues detective has identified on his travels and allow him to ask questions of the current suspect.

## Program running
There are no modules or classes created in the game. The data is set-up first. Then a continuous While True loops throug the game asking the user firstly to consider where they want to go, while at the Taxi, and once selected, identifies the suspect, item at that place and asks the user to ask about a clue. 
At the Taxi is there is an option to Quit the game. 
Options at a place are: Jaccusing the suspect, asking about Zophie the Cat, returning to the Taxi or asking about a clue listed on the screen.
The game ends when the user correctly guesses J'Accused; runs out of guesses, quits or runs out of time.

# Credits
J'ACCUSE!, by Al Sweigart al@inventwithpython.com
A mystery game of intrigue and a missing cat.
This code is available at https://nostarch.com/big-book-small-python-programming

Play the original Flash game at:
https://homestarrunner.com/videlectrix/wheresanegg.html
More info at: http://www.hrwiki.org/wiki/Where's_an_Egg%3F
