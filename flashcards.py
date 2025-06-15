import math
import os
import pandas as pd
import random

def study_cards(category):
    cards = pd.read_csv(vocab_dir + '/' + category + '.csv', encoding='utf-8')
    cards['Studied'] = False
    not_studied = cards.index[cards['Studied'] == False].tolist()
    while not_studied:
        random_row = random.choice(not_studied)
        attempts = 0
        while attempts < max_attempts:
            answer = input("\n" + str(cards.iloc[random_row][front]) + "\n")
            if answer == cards.iloc[random_row][back]:
                break
            attempts += 1
            if attempts == math.ceil(0.25 * max_attempts):
                print('Hint: ' + str(cards.iloc[random_row]['Pinyin']))
        print('The answer was: ' + str(cards.iloc[random_row][back]))
        cards.at[random_row, 'Studied'] = True
        not_studied = cards.index[cards['Studied'] == False].tolist()

root = os.getcwd()
vocab_dir = root + '/vocab/'
all_files = os.listdir(vocab_dir)
category_options = []
subcategory_options = {}
for file in all_files:
    if file.endswith('.csv'):
        category_options.append(os.path.splitext(file)[0])
    elif os.path.isdir(os.path.join(vocab_dir, file)):
        category_options.append(file)
        category_files = os.listdir(os.path.join(vocab_dir, file))
        print(category_files)
        subcategory_files = []
        for category_file in category_files:
            if category_file.endswith('.csv'):
                subcategory_files.append(os.path.splitext(category_file)[0])
        subcategory_options[file] = subcategory_files
max_attempts = 5
side_options = {0:'English', 1:'汉语'}

print("Here are the options:")
for i, file in enumerate(category_options):
    print(f"{i}. {file.capitalize()}")
category_choice = input("\nEnter your choice: ")

if category_choice.isdigit():
    category = category_options[int(category_choice)]
    if category not in subcategory_options.keys():
        for side_option in side_options:
            print(str(side_option) + ". " + str(side_options[side_option]))
        front_choice = input("\nChoose an option for the front: ")
        if front_choice.isdigit():
            front = side_options[int(front_choice)]
            back = side_options[1 - int(front_choice)]
        else:
            print("Invalid choice. \n")
        print("Loading vocabulary file for " + category + ". \n")
        study_cards(category)
    else:
        for i, file in enumerate(subcategory_options[category]):
            print(f"{i}. {file.capitalize()}")
        subcategory_choice = input("\nEnter your choice: ")
        category_path = category + '/' + subcategory_options[category][int(subcategory_choice)]
        for side_option in side_options:
            print(str(side_option) + ". " + str(side_options[side_option]))
        front_choice = input("\nChoose an option for the front: ")
        if front_choice.isdigit():
            front = side_options[int(front_choice)]
            back = side_options[1 - int(front_choice)]
        else:
            print("Invalid choice. \n")
        print("Loading vocabulary file for " + category + ". \n")
        study_cards(category_path)
else:
    print("Invalid choice. \n")

