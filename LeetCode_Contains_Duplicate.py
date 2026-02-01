"""
time_spent: 1 min (spent more time documenting alternatives and thoughts)
difficulty: easy
topic: array
problem_link: https://leetcode.com/problems/contains-duplicate/
tries: 1
created: 2026-02-01

notes:
so we are given an array of integers,
we are supposed to return true if any value appears at least twice in the array,
and false if every element is distinct
we could use a set to solve this,
create a set from the array and find it's length
if the length of the set is not equal to the length of the array, then there are duplicates
but again i wanted to be language agnostic
so i thought of sorting the array first, that would be O(n log n)
and would take O(1) space if we sort in place
then we can iterate through the array and check if any adjacent elements are equal
if they are, we return true
if we finish the loop without finding any adjacent elements that are equal, we return false
but i was like we can do better than this
since the problem space is n we should be able to solve this in O(n)
so i thought of using a hash map
we can iterate through the array and check if the element is already in the hash map
if it is, we return true
if it's not, we add it to the hash map
if we finish the loop without finding any duplicate elements, we return false
this approach takes O(n) time and O(n) space
but i was like some of us want to over engineer sometimes
i noticed you could use same approach but with a sliding window
basically, we use a set to keep track of the elements we have seen so far
then we expand the window by adding the next element to the set
if the element is already in the set, we return true
if we finish the loop without finding any duplicate elements, we return false
this approach takes O(n) time and O(n) space
you could use a hash map instead of a set, but it would take O(n) space
is there a way to do this in O(1) space?
i think if we sort the array first, we can do this in O(1) space
can we do it without sorting?
hmmm... i don't think so

time_complexity: O(n)
space_complexity: O(n)

edge_cases_tested:
- empty array
- array with one element
- array with all duplicates
- array with no duplicates
- array with mixed elements

learned:
- explore multiple approaches
- try to optimize, very important
- tyring to solve it intuitively first is good, your mind is actually smarter than you think
- after intuitive solution, write a pseudo code for it
- optimize it
- see if you can do better, play devil's advocate
- don't fall in love with your solution, yet
- pretend your worst worst enemy wrote it and try to find flaws
- this is where you start finding the edge cases
- re-evaluate your solution
- consider the time and space complexity
- then i think you're ready to go

alternatives:
- sliding window with set
- sliding window with hash map
- sorting
"""

from typing import List

class Solution:
    def contains_duplicate(self, nums: List[int]) -> bool:
        # first approach (set)
        # nums_set = set(nums) # this is O(n) time and O(n) space
        # nums_set_len = len(nums_set)
        # nums_len = len(nums)

        # the idea is;
        # if there are no duplicates, we'd have equal lengths
        # otherwise there are duplicates
        # if nums_len == nums_set_len:
        #     return False
        # else:
        #     return True
        
        # time complexity: O(n)
        # space complexity: O(n)

        # second_approach (sorting)
        # nums.sort() #this is O(n log n) time and O(1) space (in-place)
        
        # now we can iterate through the array and check if any adjacent elements are equal
        # for i in range(len(nums) - 1):
        #     if nums[i] == nums[i + 1]:
        #         return True
        # return False
        
        # time complexity: O(n log n)
        # space complexity: O(1)

        # third_approach (brute force)
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] == nums[j]:
        #             return True
        # return False
        
        # time complexity: O(n^2)
        # space complexity: O(1)

        # fourth_approach (sliding window with set)
        # seen_nums = set()

        # the idea is;
        # we expand the window by adding the next element to the set
        # if the element is already in the set, we return true
        # if we finish the loop without finding any duplicate elements, we return false
        # for i in range(len(nums)):
        #     if nums[i] in seen_nums:
        #         return True
        #     seen_nums.add(nums[i])
        # return False
        
        # time complexity: O(n)
        # space complexity: O(n)

        # fifth_approach (sliding window with hash map)
        seen_nums = {}

        # the idea is;
        # we expand the window by adding the next element to the hash map
        # if the element is already in the hash map, we return true
        # if we finish the loop without finding any duplicate elements, we return false
        for i in range(len(nums)):
            if nums[i] in seen_nums:
                return True
            seen_nums[nums[i]] = 1
        return False
        
        # time complexity: O(n)
        # space complexity: O(n)

if __name__ == "__main__":
    nums = list(map(int, input().split()))
    solution = Solution()
    result = solution.contains_duplicate(nums)
    print(result)
