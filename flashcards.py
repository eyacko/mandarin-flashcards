import math
import os
import pandas as pd
import random


def get_choice(options):
    while True:
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Enter the number.")
            continue

        if choice < 0 or choice >= len(options):
            print("Please enter a valid option. \n")
            continue
        else:
            break
    return choice


def choose_sides():
    print("\nHere are the possible card sides:")
    for side_option in side_options:
        print(str(side_option) + ". " + str(side_options[side_option]))
    front_choice = get_choice(side_options)
    front = side_options[int(front_choice)]
    back = side_options[1 - int(front_choice)]
    return front, back


def study_cards(category, subcategory = ''):
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
        correct_answer = cards.iloc[random_row][back]
        hint = cards.iloc[random_row]['Pinyin']
        attempts = 0
        while attempts < max_attempts:
            answer = input("\n" + str(prompt) + "\n")
            if answer == correct_answer:
                break
            attempts += 1
            if attempts == math.ceil(0.25 * max_attempts):
                print('Hint: ' + str(hint))
        if answer != correct_answer:
            print('The answer was: ' + str(correct_answer))
        cards.at[random_row, 'Studied'] = True
        not_studied = cards.index[cards['Studied'] == False].tolist()

root = os.getcwd()
vocab_dir = root + '/vocab/'
max_attempts = 5
side_options = {0:'English', 1:'汉语'}

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
    print(f"{i}. {file.capitalize()}")

category_choice = get_choice(category_options)
category = category_options[int(category_choice)]
if category not in subcategory_options.keys():
    front, back = choose_sides()
    study_cards(category)
else:
    print("\nHere are the subcategory options:")
    for i, file in enumerate(subcategory_options[category]):
        print(f"{i}. {file.capitalize()}")
    subcategory_choice = get_choice(subcategory_options[category])
    front, back = choose_sides()
    study_cards(category, subcategory_options[category][int(subcategory_choice)])

