"""
time_spent: 2 minutes (took a wild guess and it worked, apparently)
difficulty: easy
topic: arrays, hash tables
problem_link: https://www.geeksforgeeks.org/problems/check-if-two-arrays-are-equal-or-not3847/1
tries: 1
created: 2026-01-29

notes:
i thought of sorting both arrays and comparing them but that would take O(n log n) time, 
too much time in my opinion for this problem
i tried to think of a way to do it without using extra space but i couldn't come up with anything, 
maybe in the future
so i was like since the question says the arrays are equal if 
both contain the same set of elementts, arrangements(or permutations) of elements don't matter
i thought of using a hash table to count the frequency of each element in the first array
then i loop through the second array and decrease the frequency of each element found in the hash table
if an element is not found in the hash table, we can return false right away, 
because that means the arrays are not equal, obviously
then i realized i tried to do it by checking if a frequency becomes zero 
and trying to return false if an element is found again in the second array 
but a cleaner way is to just delete the element from the hash table when its frequency becomes zero,
then our first condition will take care of it
finally, with my approach, if the hash table is empty at the end, that means both arrays are equal, 
otherwise they are not
so we just return if the hash table is empty or not
sigh...

time_complexity: O(n + m) where n = len(a), m = len(b)
space_complexity: O(n) for the hash table storage

edge_cases_tested:
- empty arrays
- arrays of different lengths
- arrays with duplicate elements
- arrays with completely different elements

learned:
- deleting from hash table while iterating is cleaner than tracking zero frequencies
- get() method is handy for default values
- checking if hash table is empty is easier than counting remaining elements
"""

class Solution:
    def checkEqual(self, a, b) -> bool:
        a_dict = {}

        for num in a:
            a_dict[num] = a_dict.get(num, 0) + 1
        
        for num in b:
            if num not in a_dict:
                return False
            a_dict[num] -= 1
            
            if a_dict[num] == 0:
                del a_dict[num]
        
        return not a_dict

if __name__ == "__main__":
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    solution = Solution()
    result = solution.checkEqual(a, b)
    print(result)