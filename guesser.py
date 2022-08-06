
from pip import main

import random

def game():
    print("Hello! Lets play a guessing game. You need to choose a random number from 1 to 1000, and I will try to guess it! Shall we?")
    lowest = 1
    highest = 1000
    count = 0
    while True:
        guess = random.randint(lowest, highest)
        count += 1
        print(f"My guess is {guess}!")
        response = input("Tell me if I was correct(C), guessed too high(H) or too low(L)! : ").upper()
        while response not in ["C", "H", "L"]:
            response = input("Please respond with C, H or L : ").upper()
        if response == "C" or lowest == highest:
            print(f"Excellent! It took me {count} tries to guess your number, {guess}!")
            print("Thank you for playing!")
            break
        elif response == "H":
            highest = guess - 1
        elif response == "L":
            lowest = guess + 1
    print("\n")
    if input("Would you like to play again? Y if you do : ").upper() != "Y":
        exit("Goodbye!")
    else:
        print("\n\n")
        game()

if __name__ == "__main__":
    game()
