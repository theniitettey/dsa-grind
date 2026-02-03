"""
time_spent: 2 minutes (was thinking too much)
difficulty: easy
topic: implementation, arrays, strings
problem_link: https://www.hackerrank.com/challenges/python-mutations/problem?isFullScreen=true
tries: 1
created: 2026-02-03

notes:
so basically, we have a string and we need to mutate it
mutate means change a character at a specific position to a new character
there are two ways we can do this, strings are immutable in python
and in some languages, so we can't change them directly
we can:
1. Convert the string to a list, change the character, and convert it back to a string
2. Use slicing and concatenation to create a new string with the mutated character
we'll implement both approaches here
both have O(n) time complexity due to the need to create a new string
and O(n) space complexity as well
some languages may not have slicing, so the list approach is more universal
or you could use a while loop or for loop to imitate slicing
for i in range(position):
    build string up to position
then add the new character
then for i in range(position + 1, len(string)):
    build string from position + 1 to end
return the built string
this would also be O(n) time and space, and is more manual but works in any language
imitates slicing manually


time_complexity: O(n) where n = len(string)
space_complexity: O(n) since we create a new string

edge_cases_tested:
- empty string
- position at start of string
- position at end of string 

learned:
- try to imitate built-in functions manually to understand their workings
- strings are immutable in python, so mutation requires creating new strings
- think language-agnostic when solving problems to ensure broader applicability
"""

class Solution:
    def mutate_string(self, string: str, position: int, character: str) -> str:
        # 1. Convert string to list to allow mutation
        # string = list(string)

        # mutate the character at the specified position
        # string[position] = character

        # return ''.join(string)
        # this is O(n) due to the join operation
        # space complexity is also O(n) due to the list conversion
    
        # 2. Use slicing and concatenation to create the new string

        string = string[:position] + character + string[position + 1:]

        return string
        # this is also O(n) time and space due to slicing and concatenation
    

if __name__ == "__main__": 
    string = input().strip()
    position, character = input().strip().split()
    position = int(position)
    solution = Solution()
    result = solution.mutate_string(string, position, character)
    print(result)