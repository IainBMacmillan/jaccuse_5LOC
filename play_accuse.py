from state_pattern import Context, TaxiState, QuitGameState
from time import time

TIME_TO_SOLVE: int = 300  # 300 seconds (5 minutes) to solve the game


def play_accuse() -> None:
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

    start_time: float = time()
    end_time: float = start_time + TIME_TO_SOLVE

    playing = Context(TaxiState())
    while playing.is_continue():
        if time() > end_time:
            print('\nYou have run out of time! \n')
            playing.transition_to(QuitGameState())
        minutes_left: int = int(end_time - time()) // 60
        seconds_left: int = int(end_time - time()) % 60
        print('Time left: {} min, {} sec'.format(minutes_left, seconds_left))

        playing.display()
        playing.user_input()
        playing.update()


def main():
    play_accuse()


if __name__ == "__main__":
    main()
