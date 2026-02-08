"""
time_spent: 1 minute (solved part 1 of this)
difficulty: medium
topic: hash tables, hash sets, arrays
problem_link: https://leetcode.com/problems/majority-element-ii/
tries: 1
created: 2026-01-31

notes:
so unlike majority element I, here we can have up to 2 majority elements
since we are looking for elements that appear more than n/3 times
the brute force approach is straightforward
we can count the occurences of each element using nested loops
we create a first loop to pick each element
then a second loop to count how many times it appears in the array, from scratch
if the count exceeds n/3, we add it to the result
but that would be O(n^2) time complexity
we could use Boyer-Moore Voting Algorithm extension for this, but i looked at it
boy... that was getting complicated fast
so instead, we could use a hash table to count occurences of each element
then we find the elements that appear more than n/3 times
but i realized something, we create the hash table out of nums right
and in thesame iteration, we can check if the count exceeds n/3
and add it to the result
so one problem arises, we could have duplicates in the result if we add it multiple times
cos let's say an element appears 5 times, we would add it each time it exceeds n/3
so you're thinking what i'm thinking? right?
what data structure can we use to avoid duplicates?
a hash set! perfect!
so we can use a hash set to store the result
then convert it to a list before returning
this way, we avoid duplicates and keep the code simple
also we could avoid the hash set, and use a second pass to filter the hash table
but that would be less efficient
i know you taught what if we do num in result before adding
but that would be O(n) for each check, leading to O(n^2) in worst case
so using a hash set is better here or a second pass
but i like the hash set approach more for its simplicity

time_complexity: O(n) -> we traverse the list once
space_complexity: O(n) -> in the worst case, we store all elements in the hash table

edge_cases_tested:
- empty list
- list with all same elements
- list with no majority elements

learned:
- using a hash set to avoid duplicates when collecting results
- careful consideration of time complexity when checking for duplicates, the hash set and list approach we considered in the notes
- revisiting Boyer-Moore Voting Algorithm for multiple majorities
- try to see if i can understand the Boyer-Moore Voting Algorithm extension for this problem later

alternatives:
- use Boyer-Moore Voting Algorithm extension for this problem
"""

from typing import List

class Solution:
    def majority_element_ii(self, nums: List[int]) -> List[int]:
        n = len(nums)
        # result = []

        # 1. Brute force, nested loops to count each element
        # for i in range(n):
        #     num = nums[i]
        #     count = 0
        #     # we always want to count from scratch
        #     for j in range(n):
        #         if nums[j] == num:
        #             count +=  1
            # we don't want to check for duplicates yet, brute force first
            # if count > n // 3:
            #     result.append(num)
        
        # this has O(n^2) time complexity
        # however space complexity is O(1) if we don't count the output list
        
        # 2. remove duplicates from result
        # return list(set(result))

        # 3. hash table with second pass to filter
        # count = {}
        # for i in range(n):
        #     num = nums[i]
        #     if num in count:
        #         count[num] += 1
        #     else:
        #         count[num] = 1
        
        # result = []
        # now we don't necessarily need a hash set, we can do a second pass
        # this is because the hash table keys are unique
        # for key, val in count.items():
        #     if val > n // 3:
        #         result.append(key)
        
        # return result

        # 3. hash table with single pass to filter using a hash set
        count = {}
        result = set()
        for i in range(n):
            num = nums[i]
            if num in count:
                count[num] += 1
            else:
                count[num] = 1
            
            if count[num] > n // 3:
                result.add(num)
        
        return list(result)

        # this is the best approach in terms of simplicity and efficiency
        # the last two approaches have O(n) time complexity and O(n) space complexity


if __name__ == "__main__":
    solution = Solution()
    nums = list(map(int, input().strip().split()))
    result = solution.majority_element_ii(nums)
    print(result)
