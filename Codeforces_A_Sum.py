"""
time_spent: 1 minute
difficulty: easy
topic: math, implementation
problem_link: https://codeforces.com/problemset/problem/1742/A
tries: 1
created: 2026-02-06

notes:
so we are given three integers a, b, c
we need to determine if we can sum any two of them to get the third one
so we can just check the three possible combinations:
- a + b == c
- a + c == b
- b + c == a
if any of these conditions is true, we can return "YES", otherwise we return "NO
quite a straightforward implementation
however, codeforces would write a lot of wordy explanations for this problem, but the logic is pretty simple


time_complexity: O(1) since we are just doing constant time checks
space_complexity: O(1) since we are not using any extra space

edge_cases_tested:
- when a, b, c are all the same (e.g. 1, 1, 1)
- when a, b, c are all different (e.g. 1, 2, 3)

learned:
- sometimes the simplest approach is the best one
- don't overthink simple problems
- codeforces explanations can be very wordy, but the logic is often straightforward
"""

from typing import List

class Solution:
    def checkSum(self, a: int, b: int, c: int) -> str:
        if a + b == c:
            return "YES"
        elif a + c == b:
            return "YES"
        elif b + c == a:
            return "YES"
        else:
            return "NO"


if __name__ == "__main__":
    solution = Solution()
    t = int(input().strip())

    for _ in range(t):
        a, b, c = map(int, input().strip().split())
        print(solution.checkSum(a, b, c))