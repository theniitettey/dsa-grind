"""
time_spent: 1 minute (tbh)
difficulty: easy
topic: math, implementation
problem_link: https://codeforces.com/problemset/problem/546/A
tries: 1
created: 2026-02-05

notes:
so we are given the number of bananas the soldier wants to buy, 
the cost per banana, and the initial amount of money the soldier has
basically, we need to calculate the total cost of buying the bananas 
and then compare it with the initial amount of money the soldier has
we want to know if the soldier needs to borrow money, and if so, 
how much money he needs to borrow
otherwise, if the soldier has enough money, we should return 0
to calculate the total cost, we can use a loop to iterate from 1 to the number of bananas, 
and for each banana, we can calculate the cost by multiplying the cost per banana with the index of the banana 
since the cost increases with each banana
now we can compare the total cost with the initial amount of money the soldier has,
if the total cost is greater than the initial amount of money, 
we can return the difference as the amount of money the soldier needs to borrow
otherwise, we can return 0 since the soldier has enough money to buy the bananas

time_complexity: O(w) where w is the number of bananas the soldier wants to buy, since we need to calculate the cost for each banana from 1 to w.
space_complexity: O(1) since we are using a constant amount of space to store the total cost and the input values.

edge_cases_tested:
- the soldier wants to buy 0 bananas, in this case, the total cost should be 0 and the soldier should not need to borrow any money.
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