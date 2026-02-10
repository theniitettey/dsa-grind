"""
time_spent: 1 minute (tbh)
difficulty: easy
topic: strings, arrays, implementation
problem_link: https://codeforces.com/problemset/problem/71/A
tries: 1
created: 2026-02-05

notes:
so we are given a list of words, and we need to convert each word to a shorter form if it is too long
the shorter form is defined as the first letter of the word, 
followed by the number of letters between the first and last letter, 
and then the last letter of the word, returned as a string
for example, "localization" would be converted to "l10n" 
since there are 10 letters between the first and last letter
we know a word is too long if its length is greater than 10, 
so we can check the length of each word and apply the conversion if necessary


time_complexity: O(n) where n is the number of words, since we need to check the length of each word and possibly convert it.
space_complexity: O(1) since we are modifying the words in place and not using any extra space that grows with input size.

edge_cases_tested:
- words with length exactly 10, should not be converted
- words with length less than 10, should not be converted
- words with length greater than 10, should be converted

learned:
- to get an elements from the end of a string, we can use negative indexing, 
- for example, word[-1] gives us the last character of the string and word[-2] gives us the second to last character, and so on.
- this is a useful technique to remember when we need to access characters from the end of a string without needing to calculate the index based on the length of the string.
- f strings are a convenient way to format strings in Python, they allow us to embed expressions inside string literals, using curly braces {}.
- for example, f"{first}{len_between}{last}" will create a string that includes
"""

class Solution:
    def way_too_long_words(self, word: str) -> str:
        if len(word) > 10:
            first = word[0]
            len_between = len(word) - 2
            last = word[-1]

            # for python, we can use f strings
            # but we want to be language agnostic, so we can use string concatenation
            # string = f"{first}{len_between}{last}"
            string = first + str(len_between) + last
            return string
        return word


if __name__ == "__main__":
    solution = Solution()
    n = int(input().strip())
    for _ in range(n):
        word = input().strip()
        result = solution.way_too_long_words(word)
        print(result)