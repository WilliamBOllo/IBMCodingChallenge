# IBMCodingChallenge

## Code Explanation

I have created several helper function to organize the data for easier use later. Specifically, the functions
InitData, InitialAnas, jumbleCombinations, and findLetters. 

### InitData

InitData takes the command line argument of the program, which is input like this jumbleSolver.py gyrint-1-2-4,
drivet-3-6, snamea-1-6, ceedit-2-4-6, sowdah-1-4, elchek-2-6, 6-8. After the file name jumbled up words are input
with numbers coming after them symbolizing which letters will be chosen after the initial solutions. Any number
of words can be input, but the number of letters that are chosen need to match up with the number of final letters
in the solution. InitData will return something similar to {'gyrint': ['1', '2', '4'], 'drivet': ['3', '6'],
'snamea': ['1', '6'], 'ceedit': ['2', '4', '6'], 'sowdah': ['1', '4'], 'elchek': ['2', '6'], 'FAna': ['6', '8']}.
This is just a dictionary that contains the letters to be saved as values and the jumbled words as keys.


### InitialAnas

The function InitialAnas takes the initial jumbled up words, the input data, and the dataframe as input. All this
function does is organize this information and figure out all the possible anagrams that can be formed from the
input jumbles that are also words from the freq_dict. The first output from this function looks like
{'gyrint': ['trying'], 'drivet': ['divert'], 'snamea': ['seaman'], 'ceedit': ['deceit'],
'sowdah': ['shadow'], 'elchek': ['kechel', 'heckle']} which is another dictionary, but this time it takes the
initial jumbles as keys and the values are the potential words that are formed from them. The second output
is a dictionary which has the words as keys and the letters positions as values an example is
{'trying': ['1', '2', '4'], 'divert': ['3', '6'], 'seaman': ['1', '6'], 'deceit': ['2', '4', '6'],
'shadow': ['1', '4'], 'kechel': ['2', '6'], 'heckle': ['2', '6']} this makes finding the final letters much easier.

### jumbleCombinations

jumbleCombinations takes the first dictionary output from InitialAnas and creates all permutations of the words
that were generated. The output looks like [('trying', 'divert', 'seaman', 'deceit', 'shadow', 'kechel'),
('trying', 'divert', 'seaman', 'deceit', 'shadow', 'heckle')] notice how in this example the 6th words are the
only different words. This is because there were two possible words for that initial jumble and only one for
every other.

### findLetters

findLetters takes the second output of InitialAnas and the output from jumbleCombinations and returns a dictionary
that has the initial jumble combinations as keys ex. (('trying', 'divert', 'seaman', 'deceit', 'shadow', 'kechel'))
and the letters designated from each number position as values. The output will look something like
{('trying', 'divert', 'seaman', 'deceit', 'shadow', 'kechel'): 'trivtsneetsdel',
 ('trying', 'divert', 'seaman', 'deceit', 'shadow', 'heckle'): 'trivtsneetsdee'}

### FinalAnagrams

This is the main function that takes the organized information from the helper functions and generates the
final anagram or anagram phrase. Once they have all been organized they are sorted in increasing order based on
the score of the single or combined number from the frequency dictionary. Then the lowest 10 scores that are
greater than 0 are chosed from the sorted list.


## Inputs for the 5 pictures

### Input-1: jumbleSolver.py nagld-2-4-5, ramoj-3-4, camble-1-2-4, wraley-1-3-5, 3-4-4
 
### Output-1:
[['and', 'jobe', 'llew', 'llwe', 3], ['and', 'blew', 'jole', 'jole', 3], ['and', 'blee', 'jowl', 'jolw', 3],
 ['and', 'jole', 'blew', 'blwe', 3], ['and', 'jowl', 'blee', 'bele', 3], ['and', 'bowe', 'jell', 'ljle', 3],
 ['and', 'jell', 'bowe', 'obwe', 3], ['and', 'llew', 'jobe', 'jobe', 3], ['all', 'jobe', 'wend', 'ndwe', 25],
 ['all', 'jeed', 'bown', 'nobw', 25]]

This did not produce the correct answer in the 10 lowest frequency scored phrases.

### Input-2: jumbleSolver.py bnedl-1-5, idova-1-4-5, seheyc-2-6, aracem-2-6-6, 3-4-3

### Output-2:
[['dib', 'aday', 'are', 'era', 20], ['are', 'aday', 'dib', 'bid', 20], ['rib', 'aday', 'had', 'dha', 106],
 ['had', 'aday', 'rib', 'bir', 106], ['day', 'adai', 'rhb', 'bhr', 113], ['rhb', 'adai', 'day', 'dya', 113],
 ['day', 'adai', 'ber', 'ber', 113], ['day', 'adai', 'reb', 'ber', 113], ['ber', 'adai', 'day', 'dya', 113],
 ['reb', 'adai', 'day', 'dya', 113]]

This did not produce the correct answer in the 10 lowest frequency scored phrases.

### Input-3: jumbleSolver.py shast-1-4-5, doore-1-2-4, ditnic-1-2-3, catili-1-3-6, 4-8

### Output-3:
[['said', 'chorines', 'shroenic', 185], ['head', 'incisors', 'ssroinic', 689],
 ['cash', 'resinoid', 'sroeindi', 1019], ['cash', 'derision', 'sroeindi', 1019],
 ['cash', 'ironside', 'sroeindi', 1019], ['cash', 'sirenoid', 'sroeindi', 1019],
 ['rash', 'decision', 'soeindic', 1124], ['shia', 'consider', 'sroendic', 1520],
 ['shai', 'consider', 'sroendic', 1520], ['hear', 'cnidosis', 'ssoindic', 1724]]

The correct answer "rash decision" was found within the top 10, ['rash', 'decision', 'soeindic', 1124].

### Input-4: jumbleSolver.py knidy-1-2, legia-1-3, cronee-2-4, tuvedo-1-6, 8

### Output-4:
[['toddling', 0], ['addition', 1092]]

The correct answer "addition" was found, ['addition', 1092].

### Input-5: jumbleSolver.py gyrint-1-2-4, drivet-3-6, snamea-1-6, ceedit-2-4-6, sowdah-1-4, elchek-2-6, 6-8

### Output-5:

[['events', 'tiredest', 'rittsdee', 368], ['street', 'invested', 'ivntsdee', 522],
 ['veldts', 'interest', 'ritnetse', 652], ['devest', 'interest', 'ritntsee', 652],
 ['vested', 'interest', 'ritntsee', 652], ['served', 'tentiest', 'titntsee', 2423],
 ['served', 'nettiest', 'titntsee', 2423], ['denver', 'testiest', 'titstsee', 3230],
 ['tested', 'servient', 'rivntsee', 3366], ['tested', 'sirvente', 'rivntsee', 3366]]

The correct answer "vested interest" was found within the top 10, ['vested', 'interest', 'ritntsee', 652].