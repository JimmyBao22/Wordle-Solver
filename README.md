# Wordle-Solver

Program that attempts to solve Wordles. Note: the wordles being solved here are 7 letters (and therefore 7 guess attempts instead of 6).

The goal is to minimize the number of average guesses used, as well as the time it takes for a round to complete.

With the above program, the average number of guesses is around 3.6.

## Design

At every step in this game, I always want to try to choose the optimal word I can find. What is this
optimal word? Well, for every new word, I want to determine how much information it is giving me. 
The more information, the better. I want to choose the word that gives me the maximum amount of 
information at this step. 

I developed this algorithm by thinking about what information would be useful to obtain at this step.
I came to the conclusion of two specific factors: the number of new letters that this word reveals, and
the number of words that this guess eliminates (on average). 

For every single word possible at this iteration, I assign it a score. This score can be written 
as follows (the higher the sum, the better):

    Score = letter score + probability of every case * (amnt of information given (amnt of words it eliminates) by that case)

The letter score is important because by revealing more common letters, it can help with guesses on later stages.
To calculate this letter score, I found the frequencies of every letter in all_words_7.txt, leading to
a ratio between the frequency of that letter and the total amount of letters. For example, the letter
'a' occurs 11912 times, while the total number of letters across all words is 151872, leading to a ratio
of 11912:151872. The more frequent the letter, the higher score I want to assign to it because it'll more
likely help with later guesses. 

Meanwhile, for the number of words this word will eliminate, I cycle through all possibilities ('-', 'O', 'G')
for each cell, and see how many words match that possibility. The number of matches / the total number of
words left is the probability that this possibility of ('-', 'O', 'G') occurs. Then, multiply that by the number
of words it eliminates (total number of words left - number of words left if this guess is correct). Summed
over all possibilities, this basically finds the average number of words that this guess will eliminate.

Combining these two parts leads to the total score, assigned to every word that can be a possible guess
at this point in time.

I initially attempted to use this at every level, but it took too long. So, I hard coded a first and second word
that used some of the most common letters and provided good results.

For the letter score, I decided to also multiply that by a factor x. All these had around the same 
rounds per second, so I was mainly focused on average guesses. I tested a few to see which was best.
When x = 0, the average guess was around 3.75. When x = 25, the average guess was around 3.67. 
When x = 50, the average guess was around 3.62. When x = 75, the average guess was around 3.63.
When x = 100, the average guess was around 3.63. Therefore, I opted to go with x = 50.

I also tried the elimination strategy, but going two layers deep (at this step, checking all possibilities
and for each of those possibilities, checking all the future possibilities 1 layer ahead). However,
this led to worse average guesses of around 3.77 with worse rounds per second of around 0.27 (before
it was around 2).

Thus, this overall led to the completion of my algorithm.
