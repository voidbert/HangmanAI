# Hangman AI

This script tries to guess a word like it were playing Hangman. Note that this isn't intended for
the final user, since it is a command-line application.

## Usage

The program will ask for the length of the word that has to be guessed. After that, it will ask for
the positions of the most likely letter to be in the word. If it isn't in the word, leave the input
empty. If it is, write the indices of the letter's positions separated by spaces starting to count
from 1. For example, on the word banana, if the letter A is asked for, your input should be "2 4 6".
The script will keep asking for letters until the word is guessed or no words with certain letters
in the inputted positions are found.

## Custom Dictionaries

You can use custom dictionaries with this script by using their file path as the first command-line
argument (after the script's name). If no dictionary is chosen, the list of words from
[this](https://github.com/dwyl/english-words) GitHub repository will be used. This feature was
implemented so that the word lists from `/usr/share/dict` can be used without licensing problems.
These dictionaries should have a different word per line and there should be no repeated words,
given that that will cause bugs.
