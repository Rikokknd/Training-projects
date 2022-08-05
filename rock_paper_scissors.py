import random

def round(player_choice):
    game_choice = random.random("R", "P", "S")
    if player_choice == "R" and game_choice == "S":
        return "P"
    elif player_choice == "P" and game_choice == "R":
        return "P"
    elif player_choice == "S" and game_choice == "P":
        return "P" 
    else:
        return "G"

if __name__ == "__main__":
    print("\nHello! This is the Rock-Paper-Scissors game. Let's go!")
    player_score, game_score, round_counter = 0, 0, 0
    bestof = int(input("How many points determine the winner? : "))
    print("Remember! Rock beats scissors, scissors beat paper, paper beats rock.")
    print("Select your hand by typing (R)ock, (P)aper or (S)cissors.\n")
    
    while player_score != bestof and game_score != bestof:
        round_counter += 1
        player_choice = input(f"Round {round_counter}. Choose your weapon! : ").upper()

        while player_choice != "R" and player_choice != "P" and player_choice != "S":
            player_choice = input("Please respond with R, P or S : ").upper()
        
        game_choice = random.choice(["R", "P", "S"])
        print(f"You used {player_choice}. I use {game_choice}.")
        
        if player_choice == "R" and game_choice == "S":
            player_score += 1
            print("You won!")
        elif player_choice == "P" and game_choice == "R":
            player_score += 1
            print("You won!")
        elif player_choice == "S" and game_choice == "P":
            player_score += 1
            print("You won!")
        elif player_choice == game_choice:
            print("It's a tie!")
        else:
            game_score += 1
            print("You lost!")
        print("\n")
        # print(f"Score: You: {str(player_score)}, Me: {str(game_score)}. Rounds: {str(round_counter)}\n")

    print(f"\nGame over! {'You won!' if player_score > game_score else 'You lost!'}")
    print(f"Score: You: {str(player_score)}, Me: {str(game_score)}. Rounds: {str(round_counter)}\n")