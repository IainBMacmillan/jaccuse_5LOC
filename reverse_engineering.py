# DEBUGGING ROUTINES
def show_clues(clues: dict, suspects: list) -> None:
    for i, interviewee in enumerate(suspects):
        print(f'interviewee: {interviewee}')
        for c, clue in enumerate(clues[interviewee]):
            print(f'          {clue} : {clues[interviewee][clue]}')
        print()


def show_zophie_clues(clues: dict, suspects: list) -> None:
    print('Show who knows something about Zophie')
    for i, interviewee in enumerate(suspects):
        print(f'     {interviewee}:  {clues[interviewee]} ')
    print()


def main() -> None:
    # show_clues()
    pass


if __name__ == '__Main__':
    main()
