"""
time_spent: ?
difficulty: easy
topic: arrays, strings
problem_link: https://leetcode.com/problems/check-if-one-string-swap-can-make-strings-equal/
tries: 1
created: 2026-02-03

notes:
so we are given two strings and we need to check if we can make them equal
by swapping exactly one pair of characters in one of the strings
this is how i thought about it:
first, if the lengths of the strings are different, we can immediately return false
quite obvious, no?
next, sometimes the strings are already equal, 
in which case we return true
also quite obvious
now the interesting part,
we have achieved something at this point,
which is identifying that the strings are of equal length
initailly, i thought of counting character frequencies,
but that would not be sufficient,
because we need to ensure that only one swap can make them equal
then i tried thinking about it in my head,
i tried solving it mentally with examples
and tried to do exactly what my brain was doing
i noticed that, if we can indeed check if one swap can make them equal,
we need to find positons where the characters differ
let's assume there are exactly two such positions
meaning some index at s1 and some index at s2
would be different, other than these two positions, all characters would be the same
now we need to do something else, we need to remember these positions
so we can store them in a list
now per the question, we can only swap once
so if there are more than two differing positions, we can return false
i thought of early stopping once we find more than two differing positions
we could use a counter for that, and break early if it exceeds 2
now if there are exactly two differing positions, we need to check if swapping the characters at these positions would make the strings equal
so we can check if s1[pos1] == s2[pos2] and s1[pos2] == s2[pos1]
if this condition holds, we can return true, otherwise false
if you don't use the counter,
after the loop, you can check the length of the list of differing positions
if it's not 2, return false
but that adds some extra time complexity due to the list length check, so the counter approach is more efficient

time_complexity: O(n) where n = len(s1) since we traverse both strings once
space_complexity: O(1) since we use a fixed amount of extra space for the counter and positions

edge_cases_tested:
- strings of different lengths
- strings already equal
- strings differing at exactly two positions where swap makes them equal
- strings differing at more than two positions

learned:
- try to simulate mental problem solving in code
- your first thoughts are often on the right track
- your brain is smarter than you think
- early stopping can optimize performance
- think through the problem with examples before coding
- consider edge cases explicitly
"""


class Solution:
    def check_if_one_string_swap_can_make_strings_equal(self, s1: str, s2: str) -> bool:
        # base case: if lengths differ, return false
        if len(s1) != len(s2):
            return False
        
        # if strings are already equal, return true
        if s1 == s2:
            return True
        
        # 1. Differing positions approach, without counter for early stopping 
        differing_positions = []
        n = len(s1)

        # iterate through both strings to find differing positions
        # for i in range(n):
        #     if s1[i] != s2[i]:
        #         differing_positions.append(i)
        
        # if there are not exactly two differing positions, return false
        # if len(differing_positions) != 2:
        #     return False
        
        # 2. Differing positions approach, with counter for early stopping
        count_differences = 0
        for i in range(n):
            if s1[i] != s2[i]:
                count_differences += 1
                differing_positions.append(i)
                # early stopping if more than 2 differences found, O(1) operation
                if count_differences > 2:
                    return False

        # get the two differing positions
        pos1, pos2 = differing_positions[0], differing_positions[1]

        can_swap_make_equal = False
        # check if swapping the characters at these positions would make the strings equal
        if s1[pos1] == s2[pos2] and s1[pos2] == s2[pos1]:
            can_swap_make_equal = True
        
        return can_swap_make_equal


if __name__ == "__main__":
    s1 = input().strip()
    s2 = input().strip()
    solution = Solution()
    result = solution.check_if_one_string_swap_can_make_strings_equal(s1, s2)
    print(result)
