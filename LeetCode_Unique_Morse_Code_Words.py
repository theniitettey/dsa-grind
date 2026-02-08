"""
time_spent: 2 minutes (honestly speaking👀)
difficulty: easy
topic: arrays, hash tables, dictionaries, strings
problem_link: https://leetcode.com/problems/unique-morse-code-words
tries: 1
created: 2026-02-08

notes:
so we are given a list of words, 
and we need to find the number of unique morse code representations of these words
well... i had two approaches in mind,
the question already gave the morse code representations for each letter in a list
so we don't need to worry about that, 
the first approach was to create a hashmap of the morse code representations for each letter,
instead of using the list, the reason was i wanted kind of a straightforward way
to get the morse code for each letter in the word,
but from the second approach, we'll see it's not necessary, the list is enough
so for the first approach, after the hashmap
we create a hash set or a set to store the unique morse code representations of the words
then we iterate through each word in the input list,
for each word, we initialize an empty string to build the morse code representation of the word
then we iterate through each letter in the word,
we get the morse code for the letter from the hashmap and append it to the string
after we are done with the word, we add the morse code representation to the set
after we are done with all the words, we return the size of the set as the number
because sets only store unique values, 
so the size of the set will give us the number of unique morse code representations
the second approach is similar but instead of creating a hashmap for the morse code representations,
the list is of size 26, that is the number of letters in the English alphabet in order,
instead of a hashmap, we can directly use the list to get the morse code for each letter,
how? through the ASCII values of the letters,
we can calculate the index in the list for each letter by using the formula: index = ord(letter) - ord('a')
however i like to use an offset variable to make it more readable, so we can set offset = ord('a')
then the index for each letter will be: index = ord(letter) - offset
most languages have built in functions to get the ASCII value of a character,
so we can easily calculate the index for each letter and get the morse code from the list
this approach is more efficient and cleaner than the first approach,
then we do the same as before, we build the morse code representation for each word and add it to the set
after we are done with all the words, we return the size of the set as the number

time_complexity: O(n * m) where n is the number of words and m is the average length of the words
space_complexity: O(1) i think

edge_cases_tested:
- if the input list is empty, the result should be 0

learned:
- we can use ASCII values when we want to use math functions on characters
- this doesn't only apply to getting the index for the morse code list, 
- but also for other problems where we need to do calculations based on characters
- like finding the max character in a string, or counting the frequency of characters, etc.
"""

from typing import List

class Solution:
    def unique_morse_representations(self, words: List[str]) -> int:
        n = len(words)
        unique_morse_codes = set()
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        # # 1. Using hash map
        # morse_code_map = {
        #    "a":".-",
        #    "b":"-...",
        #    "c":"-.-.",
        #    "d":"-..",
        #    "e":".",
        #    "f":"..-.",
        #    "g":"--.",
        #    "h":"....",
        #    "i":"..",
        #    "j":".---",
        #    "k":"-.-",
        #    "l":".-..",
        #    "m":"--",
        #    "n":"-.",
        #    "o":"---",
        #    "p":".--.",
        #    "q":"--.-",
        #    "r":".-.",
        #    "s":"...",
        #    "t":"-",
        #    "u":"..-",
        #    "v":"...-",
        #    "w":".--",
        #    "x":"-..-",
        #    "y":"-.--",
        #    "z":"--.."
        # }

        # for i in range(n):
        #     # pick a word from the list
        #     word = words[i]
        #     # initialize an empty string to build the morse code representation of the word
        #     morse_code = ""
        #     m = len(word)
        #     # iterate through each letter in the word and append the morse code for the letter to the string
        #     for j in range(m):
        #         letter = word[j]
        #         morse_code += morse_code_map[letter]

        #     # add the morse code representation to the set
        #     unique_morse_codes.add(morse_code)

        # return len(unique_morse_codes)

        # 2. Using list and ASCII values
        morse_code_list = [
            ".-","-...","-.-.","-..",".","..-.",
            "--.","....","..",".---","-.-",".-.."
            ,"--","-.","---",".--.","--.-",".-.",
            "...","-","..-","...-",".--","-..-",
            "-.--","--.."
            ]
        
        offset = ord('a')  
        # ASCII value of 'a' is 97
        # the offset will help us calculate the index for each letter in the morse code list
        # for "a" we will get index 0, so morse_code_list[0] will give us the morse code for "a"
        # and this approach gives us zero index values
        # so we don't have to worry about negative indexes or out of range errors

        for i in range(n):
            word = words[i]
            morse_code = ""
            m = len(word)
            for j in range(m):
                letter = word[j]
                index = ord(letter) - offset
                morse_code += morse_code_list[index]

            unique_morse_codes.add(morse_code)

        return len(unique_morse_codes)       


if __name__ == "__main__":
    solution = Solution()
    n = int(input())
    words = []
    for _ in range(n):
        words.append(input())
    result = solution.unique_morse_representations(words)
    print(result)
