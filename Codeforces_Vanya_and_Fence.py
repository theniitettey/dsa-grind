"""
time_spent: 2 minutes (was thinking too much)
difficulty: easy
topic: implementation, arrays
problem_link: https://codeforces.com/problemset/problem/677/A
tries: 1 (used a similar approach as previous problems)
created: 2026-02-02

notes:
so basically a group of friends want to go past a fence
the fence has a height h
each friend has a height
if a friend's height is less than or equal to h
they can go through a width of 1
if a friend's height is greater than h
they need to bend and go through a width of 2
we need to calculate the minimum width of the fence
we can do this by iterating through the heights
and for each height, check if it's greater than h or not
and add to the min_width accordingly
if height > h, add 2 else add 1
finally return the min_width
yeah that's it



time_complexity: O(n) where n = len(heights)
space_complexity: O(1) constant space for min_width variable

edge_cases_tested:
- all heights less than or equal to h
- all heights greater than h

learned:
- straightforward implementation problems are good for warming up
- codeforces problems often have simple logic behind them, but require careful reading
- always read the problem statement carefully to understand the requirements
- you can discover patterns in the examples that help in formulating the solution
"""

from typing import List

class Solution:
    def min_fence_width(self, n: int, h: int, heights: List[int]) -> int:
        min_width = 0

        for i in range(n):
            height = heights[i]
            if height > h:
                min_width += 2
            else:
                min_width += 1
        
        return min_width


if __name__ == "__main__": 
    n, h = map(int, input().split())
    heights = list(map(int, input().split()))
    solution = Solution()
    result = solution.min_fence_width(n, h, heights)
    print(result)