INPUT_FILENAME = "./input.txt"
PART = 2

scores = {
    "A X" : 3+1,        # draw + rock
    "A Y" : 6+2,        # win + paper
    "A Z" : 0+3,        # loss + scissors
    "B X" : 0+1,        # loss + rock
    "B Y" : 3+2,        # draw + paper
    "B Z" : 6+3,        # win + scissors
    "C X" : 6+1,        # win + rock
    "C Y" : 0+2,        # loss + paper
    "C Z" : 3+3,        # draw + scissors
}

scores_2 = {
    "A X" : 0+3,        # lose with rock -> scissors
    "A Y" : 3+1,        # draw with rock -> rock
    "A Z" : 6+2,        # win with rock -> paper
    "B X" : 0+1,        # lose with paper -> rock
    "B Y" : 3+2,        # draw with paper -> paper
    "B Z" : 6+3,        # win with paper -> scissors
    "C X" : 0+2,        # lose with scissors -> paper
    "C Y" : 3+3,        # draw with scissors -> scissors
    "C Z" : 6+1,        # win with scissors -> rock
}

if __name__ == "__main__":
    with open(INPUT_FILENAME) as f:
        lines = f.read().splitlines()

    score = 0
    for line in lines:
        if(PART == 1):
            score += scores[line]
        elif(PART == 2):
            score += scores_2[line]
    print(f"Final score is: {score}")