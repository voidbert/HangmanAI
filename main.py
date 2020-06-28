import os
import sys

#A function that clears the screen
def clear_screen():
	#Use the "cls" command on Windows and the "clear" command on other systems.
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

#Prints the word that the user is guessing with underscores for unknown letters.
def print_word(word):
	#Space characters from each other and make all letters upper-case.
	to_print = ""
	for character in word:
		to_print += character.upper() + " "
	clear_screen()
	print(to_print + "\n")

#The function that loads the file with all the words
def load_words(filepath):
	#Open the file with all the words in it.
	try:
		file = open(filepath)
		#Read all the contents of the file and close it
		contents = file.read()
		file.close()
	except:
		#Failed to load the dictionary. Stop the program and warn the user.
		print("Unable to open the dictionary file. Stopping . . .")
		exit()

	#The file was loaded successfully. Because there is a different word on every line, split the
	#file by lines.
	contents = contents.splitlines()
	#Make every word lower-case (because there's no distinction between upper and lower case letters
	#in hangman).
	return [val.lower() for val in contents]

#This function takes in a list of words and asks the user for a length. Only words with that length
#will be returned.
def filter_by_length(words):
	#Try to get an integer input from the user. Keep trying until the value provided is a valid
	#integer.
	while True:
		input_string = input("Insert the length of the word: ")
		#Try to convert the string to an integer.
		try:
			clear_screen()
			input_integer = int(input_string)
			#Filter the words with only the length the user inputted.
			words_tmp = [word for word in words if len(word) == input_integer]
			#If there are no words with that length, ask for it again. Otherwise, return the list of
			#words.
			if len(words_tmp) != 0:
				return words_tmp
		except:
			#Failed to convert the string to an integer. Keep trying.
			pass

#This function guesses the most common letter in a list of words. It is the most likely letter to be
#in the word being guessed. If some letters have already been shown to the user, don't suggest them
#again.
def most_likely_letter(words, letters_to_exclude):
	#Create a dictionary to store the number of occurrences of every character.
	characters = {}
	#Register the number of occurrences of every character in all the words. Don't register already
	#suggested letters.
	for word in words:
		for character in word:
			if character not in letters_to_exclude:
				#If there isn't an entry for this character, create it
				if character in characters.keys():
					characters[character] += 1
				else:
					characters[character] = 1
	#Return the character with the most occurrences
	return max(characters, key=characters.get) 

#Asks the user where a letter is in the word and processes that input. Returns the indices of where
#that character is in the string (or False if the function failed)
def letter_location(letter, guessed_word):
	#Ask where the letter is and split all the indices
	string_input = input("Indices of the letter " + letter + ": ")
	indices = string_input.split(" ")
	#Remove all empty strings from indices (because the user can leave the input black if the
	#character isn't present in the word or the user might accidentally insert 2 spaces)
	indices = [value for value in indices if value != ""]
	for i in range(0, len(indices)):
		try:
			#Remove one from the index (the 1st character has index 0 on a string)
			indices[i] = int(indices[i]) - 1
			if (0 <= indices[i] < len(guessed_word)) == False or guessed_word[indices[i]] != "_":
				#The index isn't inside the word or the character has already been set yet. Raise an
				#exception.
				raise Exception()
		except:
			#Invalid index. Return False.
			return False
	#All indices were valid. Return them.
	return indices

#Edits the guessed word by adding the suggested letter in the locations inputted by the user and
#returning that result.
def edit_string(letter, locations, guessed_word):
	#Convert the string to an list to edit it
	lst = list(guessed_word)
	#Do all changes to the string
	for location in locations:
		lst[location] = letter
	#Convert the list back to a string and return it.
	return "".join(lst)

#Returns the list of words (subset of the inputted list) that follow the condition of having the
#newest letter in the inputted locations (or not having it)
def filter_by_condition(words, letter, locations):
	#If there are no instances of the character, return the words that don't have it.
	if len(locations) == 0:
		return [word for word in words if letter not in word]
	else:
		filtered = []
		#Add all the words that follow the condition to the list
		for word in words:
			fits_criteria = True
			for i in range(0, len(word)):
				#If this is a location where the character should be and it isn't there, this word
				#doesn't fit the criteria
				if word[i] != letter and i in locations:
					fits_criteria = False
					break
				#If the letter exists out of the locations, this word has to be removed.
				elif word[i] == letter and i not in locations:
					fits_criteria = False
					break

			#If this words fits all the conditions (letter in the locations), add it to the filtered
			#word list.
			if fits_criteria:
				filtered.append(word)
		#Return the list of filtered words
		return filtered

#The entry point of the program
def main():
	#The first argument should be processed as the file with the words. If nothing is set, words.txt
	#should be used.
	filepath = "words.txt"
	if len(sys.argv) == 2:
		filepath = sys.argv[1]

	#Clear the screen to start the game
	clear_screen()

	#Load the dictionary and ask the user for the length of the word being guessed
	words = load_words(filepath)
	words = filter_by_length(words)

	#Start the game loop. Keep track of the letters already shown to the user and the word guessed.
	guessed_word = "_" * len(words[0])
	letters_suggested = []
	while True:
		#If the number of words reached 0, there are no possible words left
		if len(words) == 0:
			clear_screen()
			print("No possible words left. Stopping . . .")
			exit()
		elif len(words) == 1:
			#There's only one possible word left.
			clear_screen()
			print("The word is: " + words[0].upper())
			exit()

		#Print the current word after clearing the screen.
		print_word(guessed_word)
		#Calculate the most-likely letter in the words and ask the user where it is in the word.
		likely = most_likely_letter(words, letters_suggested)
		#Ask where that letter is (if it is in the word)
		locations = letter_location(likely, guessed_word)
		if locations != False:
			#If finding the letter location didn't succeed, try again. Otherwise, fill the word with
			#the new characters.
			guessed_word = edit_string(likely, locations, guessed_word)
			#Filter the words that follow the condition of having these letters in the right place
			#and don't have the excluded letters.
			words = filter_by_condition(words, likely, locations)
			#Set this letter as suggested.
			letters_suggested.append(likely)			

#Start the program if this file isn't being included
if __name__ == "__main__":
	main()