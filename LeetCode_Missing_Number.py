"""
time_spent: 2 minutes (don't ask me how)
difficulty: easy
topic: math, array
problem_link: https://leetcode.com/problems/missing-number/description/
tries: 1
created: 2026-01-29

notes:
so we are given an array containing n distinct numbers
ranging from 0 to n (inclusive)
we need to return the only number in the range that is missing from the array
it is guaranteed that there is only one missing number
so we could use pythonic ways to solve this
but i wanted to be language agnostic
i was like since the numbers are from 0 to n (inclusive)
first, the range is always valid
and second, we need to find the missing number in that range
so we can sum up all the numbers from 0 to n using the formula n * (n + 1) / 2
you can use an array and sum too but that would take more space
then we can sum up all the numbers in the given array
finally, we can subtract the array sum from the expected sum
the result will be the missing number



time_complexity: O(n), where n = len(nums)
space_complexity: O(1) or O(n) if using an extra array

edge_cases_tested:
- array with one element
- array with all elements except n
- array with all elements except 0



learned:
- using a formula if there's a known pattern saves time
- subtracting while looping saves space
- always consider time and space trade-offs
- look back at the problem constraints for optimization opportunities
- go through your code to find optimizations
- look at the problem to find the best time and space complexity
- this ensures you know your code can't do better than this
- and anything more than that is not optimal


alternative:
- XOR approach also achieves O(n) time and O(1) space
- however, you need to understand bitwise operations for that
- useful when overflow is a concern in some languages
- but the sum approach is more intuitive for this problem
"""

from typing import List

class Solution:
    # leetcode's function name is missingNumber, but python convention is snake_case
    # you can name it whatever you want though
    def missing_number(self, nums: List[int]) -> int:
        n = len(nums)
        # expected_sum = 0

        # for i in range(n + 1): # inclusive of n
        #     expected_sum += i

        # time complexity of above loop is O(n)
        # array_sum = 0

        # for i in range(n):
        #     array_sum += nums[i]

        # time complexity of above loop is O(n) as well

        # return expected_sum - array_sum

        # time complexity of above is O(n)  
        # total time complexity is actually O(2n)
        # but per big O notation, it's still O(n)
        # however we use extra space, i think... probably O(1) though
        # correct me if i'm wrong

        # using the formula to calcaulate the expected sum
        expected_sum = n * (n + 1) // 2

        # this removes the need for using the first loop to calculate expected_sum, so now this is O(1) at this point

        # but then we can just subtract while looping through the array
        # this saves us from using extra space for array_sum

        for i in range(n):
            expected_sum -= nums[i]
        
        # time complexity of above loop is O(n)
        # now expected_sum holds the missing number
        # total time complexity is O(n)
        # space complexity is O(1)
        # ps: you can't do better than this in terms of time and space complexity      
        return expected_sum

if __name__ == "__main__":
    nums = list(map(int, input().split()))
    solution = Solution()   
    result = solution.missing_number(nums)
    print(result)