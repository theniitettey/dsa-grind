"""
time_spent: 2 minutes
difficulty: medium
topic: hash tables, arrays, hashing
problem_link: https://leetcode.com/problems/group-anagrams/
tries: 1
created: 2026-02-09

notes:
so we are given an array of strings and we need to group anagrams together
anagrams are words that have the same characters with same frequency but in different order
there are two common approaches to solve this problem:
1. sorting each string and using the sorted string (as a tuple) as a key in a hash table
2. counting the frequency of each character in the string, hashing it, and using that hash as a key in a hash table
for the first approach, 
we can sort each string and convert it to a tuple (since lists can't be keys in a hash table) 
and use that as a key in a hash table where the value is a list of anagrams
so when we encounter a string, we sort it, convert to tuple, 
and check if it's already a key in the hash table
if it is, we append the original string to the list of anagrams for that key
if it's not, we create a new key with the sorted tuple and initialize the value with a list containing the original string
so from this we expect the hash table to be tuple(sorted_string) : [list of anagrams]
after processing all strings, we can return the values of the hash table as a list of 
this uses 0(n k log k) time complexity 
where n is the number of strings and k is the average length of the strings (due to sorting)
for the second approach,
we can count the frequency of each character in the string,
for this we use ASCII values and a list of size 26,
so we basically do count[ASCII(char) - ASCII('a')] += 1 for each character in the string
then we convert this to a string and use it as a key in the hash table
but then we face an issue, different strings might have different counts but would produce the same count string
for edample, "abb" and "aab" would both produce "1a2b0c0d...0z", this is called a hash collision
and it will cause us to group non-anagrams together, which is incorrect
so we need to make sure the count string is unique for each anagram group,
one of the easiest way to do this is to include a separator between counts, 
for example we can use "#" as a separator  or make a characjter count string like "a1b2c0d0...z0"
i decided to go with the "#" separator approach, 
and this ensures that the count string is unique for each anagram group,
so we can use this count string as a key in the hash table and group anagrams together
for every string, we compute the count string and use it as a key in the hash table
if the key already exists, we append the original string to the list of anagrams for that key
if it doesn't exist, we create a new key with the count string 
and initialize the value with a list containing the original string
after processing all strings, we can return the values of the hash table as a list of lists

time_complexity: O(n * k) where n is the number of strings and k is the average length of the strings (due to counting characters)
space_complexity: O(n * k) in the worst case if all strings are anagrams of each other, we would have n strings in one group and the count string would be of length k

edge_cases_tested:
- empty array
- array with one string
- array with all strings being anagrams of each other
- array with no anagrams (all strings are unique)

learned:
- hash collisions can occur when different inputs produce the same hash key, 
- which can lead to incorrect grouping in problems like this
- to avoid hash collisions, we can use a unique representation of the input as the key in the hash table
- for example, using a separator in the count string ensures that different character counts produce different keys
- when using a hash table to group items, the key should uniquely identify the group
"""

from typing import List

class Solution:
    def group_anagrams(self, strs: List[str]) -> List[List[str]]:
        n = len(strs)
        anagram_groups = {}
        result = []
        # # 1. Sorting approach
        # for i in range(n):
        #     # pick a word
        #     word = strs[i]
        #     # sort the word and convert to tuple
        #     sorted_word = tuple(sorted(word))
        #     # use the sorted tuple as key in hash table
        #     if sorted_word in anagram_groups:
        #         anagram_groups[sorted_word].append(word)
        #     else:
        #         anagram_groups[sorted_word] = [word]
        
        # # append the values of the hash table to result
        # for group in anagram_groups.values():
        #     result.append(group)

        # return result
        # # time complexity: O(n * k log k) due to sorting each string
        # # space complexity: O(n * k) in the worst case

        # 2. Counting approach with separator to avoid hash collisions
        for i in range(n):
            word = strs[i]
            count = [0] * 26  # count of each character
            for char in word:
                count[ord(char) - ord('a')] += 1
            
            # create a count string with separator to avoid hash collisions
            count_string = "#".join(str(c) for c in count)
            
            if count_string in anagram_groups:
                anagram_groups[count_string].append(word)
            else:
                anagram_groups[count_string] = [word]
        
        # append the values of the hash table to result
        for group in anagram_groups.values():
            result.append(group)

        return result
        # time complexity: O(n * k) due to counting characters in each string
        # space complexity: O(n * k) in the worst case


if __name__ == "__main__":
    solution = Solution()
    n = int(input().strip())
    strs = []
    for _ in range(n):
        s = input().strip()
        strs.append(s)
    result = solution.group_anagrams(strs)
    print(result)
