"""
time_spent: 2 minutes (maybe 5 more... idk)
difficulty: easy
topic: strings, hash sets
problem_link: https://leetcode.com/problems/keyboard-row/
tries: 1
created: 2026-02-05

notes:
so we are given a list of words
and rows of an american keyboard
we are to find the words that can be typed using letters of the alphabet on only one row of the keyboard
to solve this problem, we can use hash sets to represent the three rows of the keyboard
we can then iterate through each word in the input list and check if all characters of the word belong to one of the three hash sets
we can maintain a count of how many characters of the word belong to each row
if the count for any row equals the length of the word, it means all characters of the word belong to that row and we can add it to our result list
this approach is efficient since checking membership in a hash set is O(1) on average,
and we only need to iterate through each word and its characters once


time_complexity: O(n * m) where n = number of words and m = average length of each word
space_complexity: O(1) since the size of the hash sets is constant and does not grow with input size

edge_cases_tested:
- empty list
- words with mixed case letters
- words with non-alphabetic characters (not specified in problem, but good to consider)

learned:
- a hash table stores key-value pairs, while a hash set only stores keys
- hash set is useful for membership testing and eliminating duplicates
- and a hash set is basically just a set in python, the syntax just caught me off guard
- because i'm used to set()
- also just intializing an empty {} creates a hash table not a hash set👀
"""

from typing import List

class Solution:
    def keyboard_row(self, words: List[str]) -> List[str]:
        row1 = {"q", "w", "e", "r", "t", "y", "u", "i", "o", "p"}
        row2 = {"a", "s", "d", "f", "g", "h", "j", "k", "l"}
        row3 = {"z", "x", "c", "v", "b", "n", "m"}
        result = []
        
        n = len(words) 

        for i in range(n):
            row1_count = 0
            row2_count = 0
            row3_count = 0

            word = words[i].lower()

            for char in word:
                if char in row1:
                    row1_count += 1
                elif char in row2:
                    row2_count += 1
                elif char in row3:
                    row3_count += 1
            
            if row1_count == len(word) or row2_count == len(word) or row3_count == len(word):
                result.append(words[i])

        return result


if __name__ == "__main__":
    solution = Solution()
    t = int(input())
    words = []
    for _ in range(t):
        word = input()
        words.append(word)
    result = solution.keyboard_row(words)
    print(result)
