"""
time_spent: 1 minute (had some higher revelations)
difficulty: easy
topic: arrays, dictionaries
problem_link: https://leetcode.com/problems/two-sum/
tries: 1
created: 2026-01-30

notes:
so the question says given an array of integers nums and an integer target
we need to find two numbers in nums such that they add up to target
we can't use the same element twice
we need to return the indices of the two numbers
so i thought of a brute force approach with nested loops
where we start a first loop at i to n, then
i run a second loop from i + 1, n, gives us j
i + 1 because we can't use the same element twice
we're finding if nums[i] + nums[j] == target, if so return [i, j]
but that would be O(n^2) time complexity, which is not optimal
so i thought of optimizing this further
if we have a num i and we want to find some num j that adds to target
i.e i + j = target, we can rearrange to find j = target - i
meaning for each num in nums, we can calculate the complement and (drum roll)
we store the nums we've seen so far in a dictionary as num: index pairs
if we have seen the complement before, we can return the indices
but the indices and return part can be confusing
so we stored nums[i] = i in the dictionary right, so this would be first index
then we check if complement in num_to_index
if it is, we return [num_to_index[complement], i]
num_to_index[complement] gives us the index of the complement which is the first index
and i is the current index in the loop which is the second index
so basically, this approach is O(n)
we just use extra space to store the complements in a dictionary
but it's worth it for the time complexity improvement
i wish there was a way to do it in O(n) time and O(1) space
but i don't think it's possible without modifying the input array
maybe if the array was sorted we could use two pointers
don't worry about that for now though
ps: you should probably check two pointers out tho

time_complexity: O(n)
space_complexity: O(n) for the dictionary storage

edge_cases_tested:
- empty array
- array with one element
- array with negative numbers
- array with multiple valid pairs (should return first found)

learned:
- try to figure out a work around for brute force approaches
- using a dictionary to store complements for O(1) lookups
- rearranging equations to find complements
- careful with indices when returning results
- always check if the dictionary contains the complement before adding current num
ps: for some reason, i forget the last point sometimes
"""

from typing import List

class Solution:
    def two_sum(self, nums: List[int], target: int) -> List[int]:
        # we could use a brute force approach with nested loops
        # where we start a first loop at i to n
        # run a second loop from i + 1, n, gives us j
        # we can't use thesame element twice
        # we're finding if nums[i] + nums[j] == target
        # if so return [i, j]


        n = len(nums)
        # for i in range(n): # this is O(n)
        #     for j in range(i + 1, n): # this is O(n) too
        #         if nums[i] + nums[j] == target:
        #             return [i, j]
        
        # total time complexity is O(n^2) for this approach
        # space complexity is O(1)
        # return []


        # we could optmize this further
        # if we have a num i and we want to find some num j that adds to target
        # i.e i + j = target, we can rearrange to find j = target - i
        # meaning for each num in nums, we can calculate the complement
        # and check if we've seen it before using a dictionary
        # if we have seen it before, we can return the indices
        # so the dictionary stores num: index pairs
        num_to_index = {}

        for i in range(n):# this is O(n)
            complement = target - nums[i] # O(1) operation
            if complement in num_to_index: # O(1) average time complexity for dict lookup
                return [num_to_index[complement], i]
            num_to_index[nums[i]] = i # O(1) average time complexity for dict insertion
        
        # total time complexity is O(n) for this approach
        # space complexity is O(n) for the dictionary storage
        return []


if __name__ == "__main__":
    nums = list(map(int, input().split()))
    target = int(input())
    solution = Solution()
    result = solution.two_sum(nums, target)
    print(result)
