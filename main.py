# Calculates score of guess against a given word
# green = +2 points, yellow = +1 point, black = +0 points
def calculate_score(guess, word):
    wordscore = 0
    for i in range(0,5):
            # Adds two to score if letter is correctly guessed
            if guess[i:i+1] == word[i:i+1]:
                wordscore += 2
                if i<len(word)-1:
                    word = word[:i] + "_" + word[i+1:]
            # Checks for yellow and black letters
            else:
                for x in range(0,5):
                    if guess[i:i+1] == word[x:x+1] and guess[x:x+1] != word[x:x+1]:
                        wordscore+=1
                        if x<len(word)-1:
                            word = word[:x] + "_" + word[x+1:]
                        else:
                            word = word[:x] + "_"
    return wordscore

# Finds word with highest overall score when looking at remaining possible answers
# Word with the highest score is returned as the best guess
def best_guess(allwords, onlyresults):
    maxscore = 0
    maxword = ""
    for guess in allwords:
        score = 0
        for word in onlyresults:
            score += calculate_score(guess, word)
        if score > maxscore:
            maxscore = score
            maxword = guess
    print("I suggest " + maxword)
    print(onlyresults)

# Shortens the list of possible answers using the inputted results of the last guess
# Eliminates any words that have a blacklisted letter, don't match for green letters,
# and don't contain the yellow letters
def shorten_possible_results(enteredword, index_of_correct, new_black, index_of_yellow, onlyresults, greenletters):
    eliminated = []
    for result in onlyresults:
        # Checking for correct green letters
        for index in index_of_correct:
            if enteredword[index:index+1] != result[index:index+1]:
                eliminated.append(result)
                break

        # Checking if has any black letters
        if result not in eliminated:
            for letter in new_black:
                if letter in result and letter not in greenletters:
                    eliminated.append(result)
                    break

        # Checking if doesn't have yellow letters
        if result not in eliminated:
            for index in index_of_yellow:
                if enteredword[index:index+1] == result[index:index+1] or enteredword[index:index+1] not in result:
                    eliminated.append(result)
                    break
    return list(set(onlyresults).difference(eliminated))

# Loop that prompts user for guess and result while giving recommendations
# Keeps track of green, yellow, and black letters
def playgame(allwords, onlyresults):
    enteredword = ""
    greenletters = []
    while(True):
        enteredword = input("What word did you guess (DONE to end): ")
        if enteredword.upper() == "DONE":
            break
        enteredresult = input("Enter result in 5 letter string (g=green, y=yellow, b=black, ex: gybby): ")
        if enteredresult.lower() == "ggggg":
            print("Congrats! Make sure to come back tomorrow!")
            break

        #finding all indices of correct letters (make function later)
        index_of_correct = [i for i, j in enumerate(enteredresult) if j == "g"]
        for i in index_of_correct:
            greenletters.append(enteredword[i:i+1])

        #creating list of incorrect letters
        new_black = [enteredword[i:i+1] for i, j in enumerate(enteredresult) if j == "b"]

        #keeping track of yellow indices
        index_of_yellow = [i for i, j in enumerate(enteredresult) if j == "y"]

        onlyresults = shorten_possible_results(enteredword, index_of_correct, new_black, index_of_yellow, onlyresults, greenletters)
        best_guess(allwords, onlyresults)

def main():
    #importing lists of all legal guesses and all possible words
    allfile = open('wordle_legal.txt', 'r')
    allwords = allfile.readlines()

    legalfile = open('wordle_solutions.txt', 'r')
    onlyresults = legalfile.readlines()

    #removing all spaces from onlyresults list
    temp = []

    for word in onlyresults:
        temp.append(word.strip())
    onlyresults = temp

    #removing all spaces from allwords list
    temp = []

    for word in allwords:
        temp.append(word.strip())
    allwords = temp
    #best_guess(allwords, onlyresults)
    
    playgame(allwords, onlyresults)

main()
