"""
time_spent: 3 mins (i wanted to understand the Boyer-Moore Voting Algorithm too)
difficulty: easy
topic: arrays, hash tables, voting algorithm
problem_link: https://leetcode.com/problems/majority-element/description/
tries: 1
created: 2026-01-30

notes:
so we are given an array of integers, of size n
we are supposed to return the majority element
the majority element is the element that appears more than n/2 (floor) times
the problem guarantees that the majority element always exists in the array
we can use a hash table to store the counts of each number
we can iterate through the array and for each number, we check if it's in the hash table
if it is, we increment its count
if it's not, we add it to the hash table with a count of 1
after updating the count, we check if the count is greater than n/2
if it is, we return the number
this approach takes O(n) time and O(n) space
but can we do better than O(n) space?
we can use the Boyer-Moore Voting Algorithm
the idea is to maintain a count and a candidate
we initialize the count to 0 and the candidate to None
we iterate through the array
for each number, if the count is 0, we set the candidate to the current number
then we check if the current number is equal to the candidate
if it is, we increment the count
if it's not, we decrement the count
at the end of the iteration, the candidate will be the majority element
this approach takes O(n) time and O(1) space
and ummm... try looking up the Boyer-Moore Voting Algorithm on youtube or something
why this works is a bit tricky to explain here
but the gist is that the majority element will always have a positive count at the end

time_complexity: O(n), n is the length of the input array
space_complexity: O(1)

edge_cases_tested:
- array with one element
- array with all elements the same
- array with negative and positive integers

learned:
- Boyer-Moore Voting Algorithm
- sometimes the optimal solution is not obvious
- try to think outside the box, don't be afraid to look up algorithms
- read a lot of problem solutions, helps with pattern recognition
- also read resources, you might end up finding Floyd's Tortoise and Hare algorithm somewhere else
ps: i just gave you a spoiler

alternatives:
- using sorting, we can sort the array and return the middle element, try it... idk how efficient that is
- Boyer-Moore Voting Algorithm is pretty optimal for this problem
- using divide and conquer, we can divide the array into two halves, find the majority element in each half, and then combine the results
"""
from typing import List

class Solution:
    def majority_element(self, nums: List[int]) -> int:
        n = len(nums)
        # first_approach (hash table)
        # counts = {}
        # for i in range(n):
        #     num = nums[i]
            # can use counts.get(num, 0) + 1
            # but making it more language agnostic
        #     if num in counts:
        #         counts[num] += 1
        #     else:
        #         counts[num] = 1
            
        #     if counts[num] > n // 2:
        #         return num
        
        # return -1  # this line should never be reached due to problem constraints
        # time complexity: O(n)
        # space complexity: O(n)

        # second_approach (Boyer-Moore Voting Algorithm)
        count = 0
        candidate = None
        for i in range(n):
            num = nums[i]
            if count == 0:
                candidate = num
            if num == candidate:
                count += 1
            else:
                count -= 1
        
        return candidate

        # time complexity: O(n)
        # space complexity: O(1)


if __name__ == "__main__":
    nums = list(map(int, input().split()))
    solution = Solution()
    result = solution.majority_element(nums)
    print(result)
