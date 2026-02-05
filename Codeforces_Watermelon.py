"""
time_spent: 1 minute
difficulty: easy
topic: math, implementation
problem_link: https://codeforces.com/problemset/problem/4/A
tries: 1
created: 2026-02-05

notes:
so we have a watermelon of weight w
we need to determine if we can split it into two parts
each part having even weights greater than 0
it is not necessary for the two parts to be of equal weight
so we can think about the conditions for this:
- if w is less than or equal to 2, we cannot split it into two even parts greater than 0, so the answer is "NO"
- if w is even and greater than 2, we can split it into two even parts, so the answer is "YES"
- if w is odd, we cannot split it into two even parts, so the answer is "NO"
so the logic is pretty straightforward...
i almost tried to overcomplicate by actually trying to split the weight
simulating the split
but that is unnecessary
with simulation, we can star from 2, split the weight into two parts
and check if we get some w + i which is even
then we can return "YES" and break out of the loop

time_complexity: O(1) since we are just doing constant time checks
space_complexity: O(1) since we are not using any extra space

edge_cases_tested:
- when w = 2 (minimum weight that cannot be split)
- when w = 3 (minimum odd weight)

learned:
- overcomplicating simple problems is a pitfall to avoid
- sometimes direct condition checks are sufficient
- sometimes the only thing your mind wants to do is to overcomplicate things
- don't worry, just try to see what your mind is trying to do and reel it back in
- simulations sometimes exposes the logic better, but not always necessary
"""


class Solution:
    def watermelon(self, w: int) -> str:
        # 1. Simulation approach
        # if w % 2 != 0 or w <= 2:
        #     return "NO"
        # else:
        #     # we want to simulate splitting the watermelon
        #     div = w // 2
        #     for i in range(2, div + 1):
        #         if (div + i) % 2 == 0:
        #             return "YES"
        #     return "NO"
        
        # 2. Direct condition checks, implementation approach
        if w > 2 and w % 2 == 0:
            return "YES"
        else:
            return "NO"


if __name__ == "__main__":
    solution = Solution()
    w = int(input().strip())
    result = solution.watermelon(w)
    print(result)
