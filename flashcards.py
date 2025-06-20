import argparse
import math
import os
import pandas as pd
import random

root = os.getcwd()
vocab_dir = root + '/vocab/'
side_options = {0:'English', 1:'汉语'}


def choose_sides(front_card):
    front = side_options[int(front_card)]
    back = side_options[1 - int(front_card)]
    return front, back


def study_cards(front_card, max_attempts, show_pinyin, deck_path):
    front, back = choose_sides(front_card)
    cards = pd.read_csv(deck_path, encoding='utf-8')
    cards['Studied'] = False
    not_studied = cards.index[cards['Studied'] == False].tolist()
    while not_studied:
        random_row = random.choice(not_studied)
        prompt = cards.iloc[random_row][front]
        if front == '汉语' and show_pinyin == True:
            pinyin = cards.iloc[random_row]['Pinyin']
            prompt += ', ' + str(pinyin)
        correct_answer = cards.iloc[random_row][back]
        attempts = 0
        while attempts < max_attempts:
            answer = input("\n" + str(prompt) + "\n")
            if answer == correct_answer:
                break
            attempts += 1
        if answer != correct_answer:
            print('The answer was: ' + str(correct_answer))
        cards.at[random_row, 'Studied'] = True
        not_studied = cards.index[cards['Studied'] == False].tolist()


def main():
    parser = argparse.ArgumentParser('Mandarin flashcards')
    parser.add_argument('deck_name', help='The name of the flashcard deck to study.')
    parser.add_argument('--no_pinyin', action='store_false', dest='show_pinyin', help='Show only characters.')
    parser.add_argument('--max_attempts', type=int, default=5, help='Maximum number of attempts to respond correctly.')
    parser.add_argument('--front_card', type=int, choices=[0, 1], default=1, help='0 for English and 1 for 汉语.')
    args = parser.parse_args()

    all_files = os.listdir(vocab_dir)
    deck_paths = {}
    for root, dirs, files in os.walk(vocab_dir):
        for file in files:
            if file.endswith('.csv'):
                deck_name = os.path.splitext(file)[0]
                deck_paths[deck_name] = os.path.join(root, file)
    chosen_deck = None
    for valid_deck_name in deck_paths.keys():
        if args.deck_name.lower() == valid_deck_name.lower():
            chosen_deck = valid_deck_name
    if chosen_deck is None:
        raise ValueError('No flashcard deck with name' + args.deck_name + ' found.')
    deck_path = deck_paths[chosen_deck]
    study_cards(args.front_card, args.max_attempts, args.show_pinyin, deck_path)


if __name__ == "__main__":
    main()
