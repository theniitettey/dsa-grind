"""
time_spent: 1 minute (tbh)
difficulty: easy
topic: math, implementation
problem_link: https://codeforces.com/problemset/problem/546/A
tries: 1
created: 2026-02-05

notes:



time_complexity: O(w) where w is the number of bananas the soldier wants to buy, since we need to calculate the cost for each banana from 1 to w.
space_complexity: O(1) since we are using a constant amount of space to store the total cost and the input values.

edge_cases_tested:
- empty list
- words with mixed case letters
- words with non-alphabetic characters (not specified in problem, but good to consider)

learned:
"""

class Solution:
    def soldier_and_bananas(self, number_of_bananas: int, cost_per_banana: int, initial_money: int) -> int:
        total_cost = 0

        for i in range(1, number_of_bananas + 1):
            total_cost += i * cost_per_banana

        if total_cost > initial_money:
            return total_cost - initial_money
        else:
            return 0

if __name__ == "__main__":
    solution = Solution()
    k, n, w = map(int, input().strip().split())
    result = solution.soldier_and_bananas(w, k, n)
    print(result)