class WordleSolver:

    def __init__(self):
        self.__all_words = []
        self.words_left = []
        self.used_letters = set()
        self.all_letter_count = dict()
        self.total_letters = 151872
        self.set_letter_count()
        self.get_words()


    def get_guess(self, feedback):
        """
        Make a guess for the current round of Wordle.
        :param feedback: A list of strings representing the guesses so far
        and the feedback for those guesses in the current game of Wordle.
        If feedback is empty then this is the first guess.
        The order of the elements of feedback is [feedback_1, guess_1,
        feedback_2, guess_2, ...]
        All strings are length 7.
        The feedback strings consist of G, O, and -.
        G for GREEN, correct letter in correct spot.
        O for letter in word but not in right spot.
        - for letter not in word.
        :return: A string that is in __all_words and is the next guess.
        """

        if len(feedback) == 0:
            self.words_left = self.__all_words
            self.used_letters = {'d', 'i', 's', 'r', 'a', 't', 'e'}
            return "disrate"

        if len(feedback) == 2:
            self.used_letters = {'d', 'i', 's', 'r', 'a', 't', 'e', 'g', 'u', 'n', 'l', 'o', 'c', 'k'}
            return "gunlock"
    
        # print(feedback)

        # print("Getting all Possible current words")
        self.words_left = self.get_possible_words(self.words_left, feedback)
        # print("Finished getting all Possible current words")

        # For every word that can be the next guess, check all 3^7 possibilities of feedback
        # results, and find the probability of each occurring.
        base_3 = [1, 3, 9, 27, 81, 243, 729]

        # print("Checking all words I could guess")
        best_score = -float('inf')
        best_word = None
        for word in self.words_left:
            # Calculate a score for this word. The higher the score, the better
            # print(word)

            # check how many new letters I am adding
            new_letter_score = 0
            for letter in word:
                if letter not in self.used_letters:
                    new_letter_score += self.all_letter_count[letter] / self.total_letters

            # print(new_letter_score)

            # initialize score as the number of new letters I am adding, weighted by their frequencies
            score = new_letter_score * 50 * len(self.words_left)
            # print("starting score ", score)
            for i in range(2187):
                feedback = ['-'] * 7
                sum = i
                # Find the corresponding letters at each location in the feedback array
                for j in range(6, -1, -1):
                    div = int(sum / base_3[j])
                    if div == 2:
                        feedback[j] = 'G'
                    elif div == 1:
                        feedback[j] = 'O'
                    
                    sum -= div * base_3[j]

                # check how many possible next words will be left if I guess this word next based on the feedback
                possible_next_words_left = self.get_possible_words(self.words_left, [''.join(feedback), word])

                # add to the current score variable how good this guess is AKA how many words I am eliminating
                score += (len(possible_next_words_left) / len(self.words_left)) * (len(self.words_left) - len(possible_next_words_left))

            if score > best_score:
                best_score = score
                best_word = word

        # print(best_score)
        # print("Got best word: ", best_word)
        for letter in best_word:
            self.used_letters.add(letter)
        
        return best_word


    def check_feedback_against_word(self, word, feedback, guess):
        """ 
        Checks if the current word works against the feedback
        """
        # First check against all the 'G' in feedback
        used = [False] * 7
        for i in range(7):
            # For every 'G', check that the letter in word matches guess
            if feedback[i] == 'G':
                if word[i] != guess[i]:
                    return False
                used[i] = True
        
        # Now, check against 'O'
        for i in range(7):
            # For every 'O', check that there exists a letter in word, at a different position,
            # that matches guess
            if feedback[i] == 'O':
                found_match = False
                for j in range(7):
                    if not used[j] and i != j and word[j] == guess[i]:
                        found_match = True
                        used[j] = True
                        break

                if not found_match:
                    return False

        # Now, check against '-'
        for i in range(7):
            # For every '-', check that no letter in word matches guess
            if feedback[i] == '-':
                for j in range(7):
                    if not used[j] and word[j] == guess[i]:
                        return False

        return True


    def get_possible_words(self, word_list, feedback):
        """ 
        Gets all the possible words out of all_words that are possible matches given feedback.
        """
        possible_words_left = []
        # Check all possible words
        for word in word_list:
            # Check all feedback
            passes_all_feedback = True
            for i in range(0, len(feedback), 2):
                if not self.check_feedback_against_word(word, feedback[i], feedback[i+1]):
                    passes_all_feedback = False
                    break
            
            if passes_all_feedback:
                possible_words_left.append(word)
        
        return possible_words_left


    def set_letter_count(self):
        self.all_letter_count = {'a': 11912,
                'b': 3401,
                'c': 5437,
                'd': 6413,
                'e': 18308,
                'f': 2266,
                'g': 4877,
                'h': 3579,
                'i': 11765,
                'j': 386,
                'k': 1978,
                'l': 8495,
                'm': 4254,
                'n': 9059,
                'o': 8646,
                'p': 4444,
                'q': 286,
                'r': 11339,
                's': 14029,
                't': 8642,
                'u': 5677,
                'v': 1361,
                'w': 1768,
                'x': 473,
                'y': 2451,
                'z': 626 }


    def get_words(self):
        """ Read the words from the dictionary file and place them
        in the __all_words instance variable.
        We assume the  required files are in the current working directory
        and is named all_words_7.txt. We also assume all words are
        seven letters long, one word per line.
        Returns a set of strings with all the words from the file.
        """
        with open('all_words_7.txt', 'r') as data_file:
            all_lines = data_file.readlines()
            for line in all_lines:
                self.__all_words.append(line.strip())


    def show_words(self):
        """
        Debugging method to check file was read in correctly.
        :return: None
        """
        print(len(self.__all_words))
        for word in self.__all_words:
            print(word)
