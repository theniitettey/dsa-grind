"""
time_spent: 2 minutes (tried to figure out an easier way)
difficulty: easy
topic: arrays, counting, prefix sums
problem_link: https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current_number
tries: 1
created: 2026-02-04

notes:
so we are given an array of numbers (nums)
we are to find out how many numbers
are smaller than the current number for each number in the array
and return that as an array of the same length
with some constraints:
for each nums[i], we have to count the valid j's
such that j != i and nums[j] < nums[i]
so we can do this with a brute-force approach
we can initialize an empty list to store the results
then we can loop through each number in the input array
for each number, we can initialize a count variable to 0
then we can loop through the array again and compare the current number with the other numbers
this will give us a time complexity of O(n^2) since we have nested loops
but we can optimize this using counting and prefix sums
since the constraints say 0 <= nums[i] <= 100, we can create a count array of size 101 to count the occurrences of each number
then we can create a prefix sum array to store the cumulative counts
basically we're saying up to some point or number x,
we have seen y numbers that are less than x
because after counting, the prefix sum sums up all the counts up to that index
then we can loop through the input array again
and for each number, we can directly index into the prefix sum array to get the count of numbers smaller than it
this will give us a time complexity of O(n + m) where n is the length of the input array and m is the range of numbers (which is 101 in this case)
but i think it should be O(n) since m is a constant (101), so we can say O(n) for the time complexity
and space complexity of O(m) for the count and prefix sum arrays

time_complexity: O(n) where n = the length of the input array since we loop through it a few times but the counting and prefix sum arrays are of constant size
space_complexity: O(m) where m = the range of numbers (which is 101 in this case) for the count and prefix sum arrays

edge_cases_tested:
- duplicate numbers in the input array (to check for correct counting)
- numbers at the boundaries (0 and 100) to check for correct counting and indexing

learned:
- for counting problems of no order or arrangement, counting and prefix sums can be very useful
- prefix sums can help in quickly retrieving cumulative counts
- you can have off by 1 errors usage of prefix sums, so be careful with indexing and offset when using prefix sums
- this handles the case when nums[i] is 0, we want to count how many numbers are smaller than it, which would be at index 0 in the bucket, so we offset by 1 to handle that case

alternatives:
- we could also sort the input array and
then use binary search to find the count of numbers smaller than each number, 
but that would give us a time complexity of O(n log n) due to sorting, 
which is less efficient than the counting 
and prefix sum approach for this problem
"""

from typing import List

class Solution:
    def smaller_numbers_than_current(self, nums: List[int]) -> List[int]:
        #1. Bruteforce approach
        n = len(nums)
        result = [0] * n  # initialize result list with zeros

        # for i in range(n):
        #     # initialize count variable to 0 for each number
        #     count = 0
        #     # get the current number
        #     num = nums[i]
        #     # loop through the array again to compare
        #     for j in range(n):
        #         # follow the condition j != i and nums[j] < nums[i]
        #         if i != j and nums[j] < num:
        #             count += 1
        #     # append the count to the result list
        #     result.append(count)
        
        # return result

        # this approach works but is not optimal
        # time complexity is O(n^2) due to nested loops
        # space complexity is O(1) if we don't count the output space as it is expected
            

        # 2. Optimal approach using counting and prefix sums
        bucket = [0] * 102  # since 0 <= nums[i] <= 100
        # offset by 1 to handle the case when nums[i] is 0, 
        # we want to count how many numbers are smaller than it, which would be at index 0 in the bucket

        # count the occurrences of each number in the input array
        for i in range(n):
            bucket[nums[i] + 1] += 1
        
        # find cumulative counts (prefix sums)   
        # adding from behind cummulatively because 
        # we want to know how many numbers are smaller than the current number
        for i in range(1, 102):
            bucket[i] += bucket[i - 1]
        
        for i in range(n):
            result[i] = bucket[nums[i]]

        return result
    
        # time complexity is O(n) since we loop through the input array a few times
        # space complexity is O(m) where m = 101 (constant) for the bucket array     


if __name__ == "__main__":
    solution = Solution()
    nums = list(map(int, input().strip().split()))
    result = solution.smaller_numbers_than_current(nums)
    print(result)
