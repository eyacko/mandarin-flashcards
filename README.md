# Mandarin flashcards

A simple script to practice recalling vocabulary.

## Requirements

You will need to have Python installed.

## Default behaviour

To run using the defaults, simply enter `python flashcards.py` in your terminal. You will have 5 attempts to guess each word in the selected deck. The words will be shown in Chinese characters and Hanyu Pinyin, and you will need to enter the English translation. If you answer correctly within the maximum number of attempts, the next word will be shown. Otherwise, you will be prompted again with the same word. If you do not enter the correct response within the maximum number of attempts, the correct answer will be shown and you will be prompted with the next word. The order of words is randomized each time.

## Customization

To change the maximum number of attempts, run with the command line argument `--max_attempts X`, where X is the number of desired maximum attempts. To show only the Chinese characters, run with `--no_pinyin`. To be shown English words and respond in Chinese characters, run with `--front_card 0`. Currently, there is no option to be shown English words and respond in Hanyu Pinyin.
