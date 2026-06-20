"""
time_spent: 1 minute (tbh, this is a very easy problem)
difficulty: easy
topic: strings, two pointers, arrays
problem_link: https://leetcode.com/problems/reverse-string/
tries: 1
created: 2026-06-19

notes:
we are given an array of characters, and we need to reverse the array in place. there are two common approaches to solve this problem:
- two pointers: we can use two pointers, one at the beginning of the array 
and one at the end then we can swap the characters at the two pointers 
and then move the pointers towards each other until they meet.
- built-in reverse function: we can use the built-in reverse function to reverse the array in place. 
this is a very simple and efficient solution, but it may not be allowed in some coding interviews.
and sine we want to be language agnostic, we will go with the two pointers approach.
this is an O(n) time complexity and O(1) space complexity solution.

time_complexity: O(n), we need to iterate through the array once to reverse it.
space_complexity: O(1), we are reversing the array in place, so we are not using any extra space.

edge_cases_tested:
- empty array: we should return an empty array.
- array with one character: we should return the same array.

learned:
- when to use <= or < for while loop conditions, this is how i understand it:
- ask yourself, do you want to do something with the value when both pointers meet?
- if yes, then we use <=, if no, then we use <.
- basically, <= means at meeting point, we still want to do something with the value, 
- while < means at meeting point, we don't want to do anything with the value.
- why does this matter? in some questions, especially if you're a competitive programmer
- you might want to prevent uncessary iterations or work
- for this problem, the mid point of the string, whether a value or gap, doesn't matter
- it's like the mirror point of the string, so we don't need to do anything with it for the string to be reversed,
- eg: hello, it's he l lo -> ol l eh, you realize the middle stay the same, so we don't need to do anything with it,
- eg: mama, it's ma ma -> am am, you realize the middle stay the same, so we don't need to do anything with it,
- so we can use < for the while loop condition, save us an extra iteration
"""

from typing import List

class Solution:
    def reverse_string(self, s: List[str]) -> None:
        # initialize two pointers
        # one at the beginning of the array 
        # one at the end
        begin = 0
        end = len(s) - 1

        # loop conditon: while the two pointers do not meet
        while begin < end:
            # swap the characters at the two pointers
            # this is a tuple assignment, it allows us to swap the values without using a temporary variable
            # but we want to be language agnostic, so we can use a temporary variable to swap the values
            # s[begin], s[end] = s[end], s[begin]

            swap = s[begin]
            s[begin] = s[end]
            s[end] = swap

            # move the pointers towards each other
            begin += 1
            end -= 1
        


if __name__ == "__main__":
    solution = Solution()
    s = list(input().strip())
    result = solution.reverse_string(s)
    print(s)
