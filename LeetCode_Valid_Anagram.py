"""
time_spent: 1 minute
difficulty: easy
topic: hash tables, strings
problem_link: https://leetcode.com/problems/valid-anagram/description/
tries: 1
created: 2026-02-07

notes:
so we are given two strings s and t, and we need to determine if t is an anagram of s
an anagram means that t can be formed by rearranging the letters of s,
so they must have the same characters with the same frequency
you could count the frequency of each character in both strings and compare the counts
or you could sort both strings and check if they are equal
the first is O(n) or can be O(n * m) based on the implementation, while the second is O(n log n) due to sorting
for my approach i want to use a hash table
now base cases we can check before we even start counting:
- if the lengths of s and t are different, we can immediately return false
- if s and t are the same, we can immediately return true
now that we have cleared those base cases, we can count the frequency of characters in s and t
then i thought... we can do this in two ways again
- we can make a hash table for s and a hash table for t, then compare the two hash tables, O(n) time complexity still but with more space used
or we can use my thinking, which relies on this thought process:
- we can make a hash table for s, keeping track of the frequency of characters
if t is indeed an anagram of s, it means, if we iterate the hash table we can do some magic
- if a charater in t is not in the hash table, then we can return false immediately
- else, we decrease the frequency of that character in the hash table, if that frequency becomes negative, we can return false immediately
otherwise if the frequency is zero, we can remove that character from the hash table
at the end we expect the hash table to be empty, if it is not empty, we can return false, otherwise we can return true
now the space complexity is tricky, '
you need to ask yourself, at the end of the day, would the hash table be empty?
i leave the rest to you... continue to keep the faith brave coder, you are doing great

time_complexity: O(n) where n is the length of the strings, since we are iterating through both strings once
space_complexity: read the notes

edge_cases_tested:
- when s and t are the same (e.g. "listen", "listen")
- when s and t are anagrams (e.g. "listen", "silent")
- when s and t are not anagrams (e.g. "hello", "world")
- when s and t have different lengths (e.g. "abc", "abcd")

learned:
- there are multiple ways to solve the same problem, and it's important to consider the trade-offs between time and space complexity
- sometimes you can optimize space complexity by using a single data structure instead of multiple ones
- it's important to consider edge cases and base cases before diving into the main logic of the problem
- sometimes the most straightforward approach is the best one, and you don't need to overcomplicate

alternatives:
- sorting both strings and comparing them, which is simpler but less efficient
- using two hash tables to count the frequency of characters in both strings and then comparing the hash tables
- counting the frequency of characters in s and t simultaneously in one pass, which can be more efficient but also more complex to implement
- however you can use the string.count(some_char)
"""

from typing import List

class Solution:
    def valid_anagram(self, s: str, t: str) -> bool:
        # base cases
        # 1. if the lengths of s and t are different, return false immediately
        if len(s) != len(t):
            return False
        # 2. if s and t are the same, return true immediately
        if s == t:
            return True
        
        # 1. Sorting approach
        # should i complicate, yes, why? i want to be language agnostic
        # sorted might not be available in all languages, so we implement our own sorting algorithm
        # let's write a sorted function using the easiest sorting algorithm, which is bubble sort
        # def bubble_sort(arr):
        #     n = len(arr)
        #     for i in range(n):
        #         for j in range(0, n-i-1):
        #             if arr[j] > arr[j+1]:
        #                 arr[j], arr[j+1] = arr[j+1], arr[j]
        #     return arr
        
        # # now let's convert the strings to lists of characters and sort them
        # sorted_s = []
        # sorted_t = []
        # n = len(s)
        
        # for i in range(n):
        #     sorted_s.append(s[i])
        #     sorted_t.append(t[i])
        
        # sorted_s = bubble_sort(sorted_s)
        # sorted_t = bubble_sort(sorted_t)

        # # now for the comparison, since they are sorted, we can just compare them character by character
        # for i in range(n):
        #     if sorted_s[i] != sorted_t[i]:
        #         return False
        
        # return True

        # # time complexity: O(n log n) due to the sorting step
        # # space complexity: O(n) due to the sorted lists

        # 2. hash table approach, two hash tables
        # dict_s = {}
        # dict_t = {}

        # # sometimes i understimate the power of the range function
        # # but using the for in loop makes us have to loop one iterable at a time
        # # but the for range loop allows us to loop through both iterables at the same time, 
        # # since they have same length at this point which is more efficient
        # for i in range(len(s)):
        #     char_s = s[i]
        #     char_t = t[i]

        #     if char_s in dict_s:
        #         dict_s[char_s] += 1
        #     else:
        #         dict_s[char_s] = 1
            
        #     if char_t in dict_t:
        #         dict_t[char_t] += 1
        #     else:
        #         dict_t[char_t] = 1
        
        # return dict_s == dict_t

        # time complexity: O(n) since we are iterating through both strings once
        # space complexity: O(n) in the worst case if all characters are unique

        # 3. hash table approach, one hash table
        char_count = {}
        for i in range(len(s)):
            char_s = s[i]
            
            if char_s in char_count:
                char_count[char_s] += 1
            else:
                char_count[char_s] = 1
            
            # we could use the get method to simplify the code, but i want to be language agnostic
            # char_count[char_s] = char_count.get(char_s, 0) + 1
        
        for i in range(len(t)):
            char_t = t[i]

            if char_t not in char_count:
                return False
            else:
                char_count[char_t] -= 1
                if char_count[char_t] < 0:
                    return False
                elif char_count[char_t] == 0:
                    del char_count[char_t]
        

        # we could return in two ways
        # 1. we can check if the hash table is empty, in most languges empty is Null/None/False, so we can just return not char_count
        # 2. we can check if the length of the hash table is zero, which is more explicit, but also more verbose

        return not char_count
        # time complexity: O(n) since we are iterating through both strings once
        # space complexity: i left that for you to keep the faith, remember?

if __name__ == "__main__":
    solution = Solution()
    s = input().strip()
    t = input().strip()
    result = solution.valid_anagram(s, t)
    print(result)


