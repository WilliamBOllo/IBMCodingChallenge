# -*- coding: utf-8 -*-
"""
Created on Fri Jan  31 08:40:58 2020

@author: William
"""

import sys
import re
import pandas as pd
import itertools
import json

#Function to take the input data and transform it into a dictionary
#that is easier to work with later
def InitData(ar):
    dic = {}
    for i in range(len(ar) - 1):
        tmp = []
        test = re.sub(',', '', ar[i])
        test = re.split('-', test)
        for item in test[1:len(test)]:
            tmp.append(item)
        dic[test[0]] = tmp
    if('-' in ar[-1]):
        test = re.split('-', ar[-1])
        dic["FAna"] = test
    else:
        dic["FAna"] = ar[-1]
    return dic


#Function to take the initial jumbles and return a dictionary with a key
#that is the initial jumbled words and the value being the words from
#the given frequency dictionary that are anagrams of the initial jumble
def InitialAnas(iD, dic, daF):   
    wrds = {}
    letterKey = {}
    for i in range(len(iD)):
        wrd = iD[i]
        tmpwrds = []
        perms = [''.join(perm) for perm in itertools.permutations(wrd)]
        df_anas = daF.query('Word in @perms')
        df_tmp = df_anas[df_anas['Frequency'] > 0]
        if(len(df_tmp) > 0):
            for rows in df_tmp.itertuples():
                tmpwrds.append(rows.Word)
                letterKey[rows.Word] = dic[iD[i]]
        else:
            for rows in df_anas.itertuples():
                tmpwrds.append(rows.Word)
                letterKey[rows.Word] = dic[iD[i]]
        wrds[iD[i]] = tmpwrds
    return wrds, letterKey


#Function to create a list of all the possible combinations of solved
#jumbles. This is only necessary when there are more than a single 
#answer for one or more of the initial jumbles 
def jumbleCombinations(IaL):
    key = IaL.keys()
    lists = []
    for item in key:
        lists.append(IaL[item])
    perms = list(itertools.product(*lists))
    return perms


#Function to find and return the desired letters from each of the
#solved jumbles to be used in the final larger jumble
def findLetters(JcL, lKl):
    letters = {}
    for item in JcL:
        tmp = ""
        for items in item:
            for numbers in lKl[items]:
                tmp+= items[int(numbers) - 1]
        if(tmp in letters.values()):
            continue
        else:
            letters[item] = tmp
    return letters

#This function takes a dictionary that holds the initial jumble combinations as keys and
#the corresponding letters as values. The second argument is also the order and number
#of letters the final anagram has for example, rash decisions would be 4-8. Amd fomally
#it takes the dataframe.
def FinalAnagrams(lett, Fa, dF):
    answers = []
    jcs = list(lett.keys())
    #If there is only 1 possible answer then the program can easily generate all
    #possible anagrams
    if(len(Fa) == 1):
        for item in jcs:
            perms = [''.join(perm) for perm in itertools.permutations(lett[item], int(Fa))]
            df_anas = dF.query('Word in @perms')
            for rows in df_anas.itertuples():
                if([rows.Word, rows.Frequency] not in answers):
                    answers.append([rows.Word, rows.Frequency])
        answers = sorted(answers, key = lambda x: x[-1])
        answersF = []
        if(len(answers) > 10):
            for phrase in answers:
                if(phrase[-1] > 0):
                    answersF.append(phrase)
                if(len(answersF) > 9):
                    break
            return answersF
        return answers
    else:
        #This for loop is necessary if there are more than one possible word for the
        #initially solved jumbles.
        for item in jcs:
            tmparr = [[] for x in range(len(Fa))]
            perms = [''.join(perm) for perm in itertools.permutations(lett[item], int(Fa[0]))]
            df_anas = dF.query('Word in @perms')
            for rows in df_anas.itertuples():
                if([rows.Word, lett[item]] not in tmparr[0]):
                    tmparr[0].append([rows.Word, lett[item], rows.Frequency])
            #Iterates through every word that needs to have a word generated for it
            for i in range(1, len(Fa)):
                #Iterates through the entire list of initially generated words
                for j in range(len(tmparr[i - 1])):
                    #fWord is just a list of words that has been generated so far
                    fWord = tmparr[i - 1][j][0:i]
                    #genWord is the word that is generated for letters to be subtraced
                    #from
                    genWord = tmparr[i - 1][j][len(tmparr[i - 1][j]) - 2]
                    #score is the frequency score
                    score = tmparr[i - 1][j][-1]
                    #Removes specific letters from the group of final letters at each
                    #iteration
                    for letter in fWord:
                        for let in letter:
                            genWord = genWord.replace(let, '', 1)
                    perms = [''.join(perm) for perm in itertools.permutations(genWord, int(Fa[i]))]
                    df_anas = dF.query('Word in @perms')
                    #Creates an entry for the current step to be inserted into
                    #the tmparr in the appropriate list.
                    if(len(df_anas) != 0):
                        for rows in df_anas.itertuples():
                            entry = [x for x in fWord[0:i]]
                            entry.append(rows.Word)
                            entry.append(genWord)
                            entry.append(rows.Frequency + score)
                            if(entry not in tmparr[i]):
                                tmparr[i].append(entry)
            #Moves all the possible answers from this group of initial jumbes and
            #places them all into the final answers list
            for ans in tmparr[-1]:
                answers.append(ans)
        #Sorts the entire list of possible phrase anagrams
        answers = sorted(answers, key = lambda x: x[-1])
        answersF = []
        #Grabs the first 10 entries in the sorted answers list that have a score
        #above 0
        if(len(answers) > 10):
            for phrase in answers:
                if(phrase[-1] > 0):
                    answersF.append(phrase)
                if(len(answersF) > 9):
                    break
        return answersF
                            
    

def main():
    #Opens and loads the json file into python to be converted to a series and then
    #to a dataframe for ease of anagram lookup
    with open('freq_dict.json', 'r') as f:
        data=json.load(f)
    s = pd.Series(data, name='Frequency')
    df = pd.DataFrame({'Word': s.index, 'Frequency': s.values})    
    #df = pd.read_csv('sortedTest.csv')
    #This section of code will just be setting up the information and
    #declaring specific keys from the dictionary to be used later
    IData = InitData(sys.argv[1:])
    #Initialize a list that contains all the keys for the first anagrams
    InitWords = list(IData.keys())[0: len(list(IData.keys())) - 1]
    #Initialize a variable that is set to the key for the numbeber and
    #and length of the final anagram
    FinalAna = IData[list(IData.keys())[-1]]
    #Returns a dictionary containing what I consider the most relevant
    #anagrams of the initial jumbles, also returns a dictionary that
    #contains a key with a value equal to the letters that will be used
    #in the final anagram
    Ia, lK = InitialAnas(InitWords, IData, df)
    #Returns a list of all possible initial jumble combinations
    jCs = jumbleCombinations(Ia)
    #A function to output the starter jumbles as keys and their output
    #letters as the value
    Let = findLetters(jCs, lK)
    #Finds all possible anagram combinations of the final word or phrase
    an = FinalAnagrams(Let, FinalAna, df)

    print(an)
    pass
    

if __name__ == "__main__":
    main()
    exit()