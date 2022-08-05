import random
import string

list_of_words = ["abruptly", "absurd", "abyss", "affix", "askew", "avenue", "awkward", "axiom", "azure", "bagpipes", "bandwagon", "banjo", "bayou", "beekeeper", "bikini", "blitz", "blizzard", "boggle", "bookworm", "boxcar", "boxful", "buckaroo", "buffalo", "buffoon", "buxom", "buzzard", "buzzing", "buzzwords", "caliph", "cobweb", "cockiness", "croquet", "crypt", "curacao", "cycle", "daiquiri", "dirndl", "disavow", "dizzying", "duplex", "dwarves", "embezzle", "equip", "espionage", "euouae", "exodus", "faking", "fishhook", "fixable", "fjord", "flapjack", "flopping", "fluffiness", "flyby", "foxglove", "frazzled", "frizzled", "fuchsia", "funny", "gabby", "galaxy", "galvanize", "gazebo", "giaour", "gizmo", "glowworm", "glyph", "gnarly", "gnostic", "gossip", "grogginess", "haiku", "haphazard", "hyphen", "iatrogenic", "icebox", "injury", "ivory", "ivy", "jackpot", "jaundice", "jawbreaker", "jaywalk", "jazziest", "jazzy", "jelly", "jigsaw", "jinx", "jiujitsu", "jockey", "jogging", "joking", "jovial", "joyful", "juicy", "jukebox", "jumbo", "kayak", "kazoo", "keyhole", "khaki", "kilobyte", "kiosk", "kitsch", "kiwifruit", "klutz", "knapsack", "larynx", "lengths", "lucky", "luxury", "lymph", "marquis", "matrix", "megahertz", "microwave", "mnemonic", "mystify", "naphtha", "nightclub", "nowadays", "numbskull", "nymph", "onyx", "ovary", "oxidize", "oxygen", "pajama", "peekaboo", "phlegm", "pixel", "pizazz", "pneumonia", "polka", "pshaw", "psyche", "puppy", "puzzling", "quartz", "queue", "quips", "quixotic", "quiz", "quizzes", "quorum", "razzmatazz", "rhubarb", "rhythm", "rickshaw", "schnapps", "scratch", "shiv", "snazzy", "sphinx", "spritz", "squawk", "staff", "strength", "strengths", "stretch", "stronghold", "stymied", "subway", "swivel", "syndrome", "thriftless", "thumbscrew", "topaz", "transcript", "transgress", "transplant", "triphthong", "twelfth", "twelfths", "unknown", "unworthy", "unzip", "uptown", "vaporize", "vixen", "vodka", "voodoo", "vortex", "voyeurism", "walkway", "waltz", "wave", "wavy", "waxy", "wellspring", "wheezy", "whiskey", "whizzing", "whomever", "wimpy", "witchcraft", "wizard", "woozy", "wristwatch", "wyvern", "xylophone", "yachtsman", "yippee", "yoked", "youthful", "yummy", "zephyr", "zigzag", "zigzagging", "zilch", "zipper", "zodiac", "zombie"]

def printer(_word, _letters):
    blurred_word = "".join(["*" if x in _letters else x for x in _word])
    return blurred_word

def game():
    print("\n\nHello! Let's play Hangman. I'll choose a word, and you have to guess it letter by letter!")
    max_mistakes = 9
    print(f"\nEvery time you guess a wrong letter, you lose a try. You can make {max_mistakes} errors before you lose.")
    word = (random.choice(list_of_words)).upper()
    print(f"\nI have already chose a word for you! Let's go!")

    letters = set(word)
    possible_letters = set(string.ascii_uppercase)
    used_letters = set()

    while True:
        if max_mistakes <= 0:
            print(f"\nGame over! You ran out of tries. {word} was the word. ")
            break
        if len(letters) == 0:
            print(f"\nYou won! {word} was the word!")
            break
        print(printer(word, letters))
        user_input = input("\nChoose a letter : ").upper()
        if user_input not in possible_letters or len(user_input) != 1:
            print("Please type in a single letter.")
            continue
        if user_input in used_letters:
            print("You already used this letter!")
            continue
        elif user_input not in letters:
            max_mistakes -= 1
            used_letters.add(user_input)
            print(f"You missed! You have {max_mistakes} possible mistakes left.")
            continue
        elif user_input in letters:
            print(f"Correct!")
            used_letters.add(user_input)
            letters.remove(user_input)

    if input("Would you like to play again? Y to restart: ").upper() == "Y":
        game()
    else:
        print("Goodbye!")
    
if __name__ == "__main__":
    game()