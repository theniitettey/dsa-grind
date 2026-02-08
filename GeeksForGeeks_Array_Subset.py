"""
time_spent: 5 minutes (was wondering if frequencies matter)
difficulty: easy
topic: arrays, hash tables, hash sets
problem_link: https://www.geeksforgeeks.org/problems/array-subset-of-another-array2317/1
tries: 1 (used a similar approach as previous problems)
created: 2026-01-29

notes:
so basically we need to find out whether b is a subset of a
but what exactly does that mean?
it means that all elements of b should be present in a
i wanted to make everything a hash set and use hash set operations
but i was like this should be in such a way
that it'll work if your preferred language doesn't have hash set operations
so, i thought how can i check for this
well, i can use a hash table to store the elements of a with their frequencies
then i can loop through b and check if each element is present in the hash table
and also there should be enough occurrences of each element in a to cover those in b
for early return false if any element is not found or not enough occurrences
if we finish the loop without returning false,
it means all elements of b are present in a with enough occurrences, 
so we return true
yeah so basically you can use hash sets too but this is more general
that would've been a_set.issuperset(b_set) in python
or b_set.issubset(a_set) same thing


time_complexity: O(n + m) where n = len(a), m = len(b)
space_complexity: O(n) for the hash table storage 

edge_cases_tested:
- empty arrays
- b larger than a
- arrays with duplicate elements
- arrays with completely different elements


learned:
- using a hash table to track presence is more general than hash set operations
- using hash tables for prescence is your friend when we care about duplicates
- try to think in a language agnostic way sometimes, infact all the time
- if you understand the logic, implementation in any language is easy
- think agnostically to understand
- then you can decide to use inbuilt features of a language later
- one-pass frequency checking is more efficient than building two hash tables
- decrementing counts as we go allows for early returns and saves space
"""
from typing import List
class Solution:
    def isSubset(self, a: List[int], b: List[int]) -> bool:
        a_dict = {}

        for num in a:
            a_dict[num] = a_dict.get(num, 0) + 1

        # b_dict = {}
        
        # for num in b:
        #     b_dict[num] = b_dict.get(num, 0) + 1
        
        # for num in b_dict:
        #     if num not in a_dict:
        #         return False
            
        #     if num in a_dict and b_dict[num] > a_dict[num]:
        #         return False

        # i came up with an optimized version of the above commented code
        for num in b:
            if num not in a_dict or a_dict[num] == 0:
                return False
            a_dict[num] -= 1
        
        return True


if __name__ == "__main__": 
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    solution = Solution()
    result = solution.isSubset(a, b)
    print(result)