"""
time_spent: 1 minute (this question is usually used as a warm-up)
difficulty: easy
topic: implementation, math, arrays, strings
problem_link: https://leetcode.com/problems/fizz-buzz/
tries: 1
created: 2026-02-03

notes:
so we are given a number n
and we need to return a list of strings from 1 to n
but with a twist:
- for multiples of 3, we return "Fizz"
- for multiples of 5, we return "Buzz"
- for multiples of both 3 and 5, we return "FizzBuzz"
- otherwise, we return the number itself as a string
this problem is a classic example of using conditionals and loops
usually a warmup when you have an OA on HackerRank
those OA's, sigh... we're getting there though
here's how we can implement it
we can initialize an empty list to store the results
then we can loop from 1 to n (inclusive)
for each number, we check the conditions above
then we append the appropriate string to the list
finally, we return the list
you can do some slight optimizations
the constraints say 1 <= n <= 10^4
so we can have defaults in the list
[0] * n for intialization
s[0] = "1" because index 0 corresponds to number 1
and per the problem and conditions, we will always have at least one number
so then we start our loop from 2 to n(inclusive)
but this is a minor optimization
the main logic remains the same


time_complexity: O(n) where n = the input number since we loop from 1 to n
space_complexity: O(1) becuase that is the expected output space, so technically no extra space used

edge_cases_tested:
- n = 1
- n = 15 (to check FizzBuzz case)


learned:
- classic warm-up problem
- good for practicing conditionals and loops
"""

from typing import List

class Solution:
    def fizz_buzz(self, n: int) -> List[str]:
        result = [0] * n
        # result[0] = "1"  # since we always have at least one number
        # that case start the loop from 2 to n (inclusive)

        for i in range(1, n + 1):
            if i % 3 == 0 and i % 5 == 0:
                result[i - 1] = "FizzBuzz"
            elif i % 3 == 0:
                result[i - 1] = "Fizz"
            elif i % 5 == 0:
                result[i - 1] = "Buzz"
            else:
                result[i - 1] = str(i)

        return result


if __name__ == "__main__":
    n = int(input().strip())
    solution = Solution()
    result = solution.fizz_buzz(n)
    print(result)
