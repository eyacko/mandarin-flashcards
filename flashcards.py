import argparse
import math
import os
import pandas as pd
import random

root = os.getcwd()
vocab_dir = root + '/vocab/'
side_options = {0:'English', 1:'汉语'}


def get_choice(options):
    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
        except ValueError:
            print("Enter the number.")
            continue

        if choice < 0 or choice >= len(options):
            print("Please enter a valid option. \n")
            continue
        else:
            break
    return choice


def choose_sides(front_card):
    front = side_options[int(front_card)]
    back = side_options[1 - int(front_card)]
    return front, back


def study_cards(front_card, max_attempts, show_pinyin, category, subcategory = ''):
    front, back = choose_sides(front_card)
    if subcategory:
        cards = pd.read_csv(vocab_dir + '/' + category + '/' + subcategory + '.csv', encoding='utf-8')
        print("\nLoading vocabulary file for " + subcategory + ".")
    else:
        cards = pd.read_csv(vocab_dir + '/' + category + '.csv', encoding='utf-8')
        print("\nLoading vocabulary file for " + category + ".")
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
    parser.add_argument('--no_pinyin', action='store_false', dest='show_pinyin', help='Show only characters.')
    parser.add_argument('--max_attempts', type=int, default=5, help='Maximum number of attempts to respond correctly.')
    parser.add_argument('--front_card', type=int, choices=[0, 1], default=1, help='0 for English and 1 for 汉语.')
    args = parser.parse_args()

    all_files = os.listdir(vocab_dir)
    category_options = []
    subcategory_options = {}
    for file in all_files:
        if file.endswith('.csv'):
            category_options.append(os.path.splitext(file)[0])
        elif os.path.isdir(os.path.join(vocab_dir, file)):
            category_options.append(file)
            category_files = os.listdir(os.path.join(vocab_dir, file))
            subcategory_files = []
            for category_file in category_files:
                if category_file.endswith('.csv'):
                    subcategory_files.append(os.path.splitext(category_file)[0])
            subcategory_options[file] = subcategory_files

    print("Here are the category options:")
    for i, file in enumerate(category_options):
        print(str(i) + ". " + file.replace("_", " ").capitalize())

    category_choice = get_choice(category_options)
    category = category_options[int(category_choice)]
    if category not in subcategory_options.keys():
        study_cards(args.front_card, args.max_attempts, args.show_pinyin, category)
    else:
        print("\nHere are the subcategory options:")
        for i, file in enumerate(subcategory_options[category]):
            print(str(i) + ". " + file.replace("_", " ").capitalize())
        subcategory_choice = get_choice(subcategory_options[category])
        study_cards(args.front_card, args.max_attempts, args.show_pinyin, 
                    category, subcategory_options[category][int(subcategory_choice)])


if __name__ == "__main__":
    main()
