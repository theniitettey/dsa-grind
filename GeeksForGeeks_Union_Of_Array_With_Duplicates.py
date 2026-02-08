"""
time_spent: 1 minutes (doesn't mean i'm a genius)
difficulty: easy
topic: hash sets, arrays
problem_link: https://www.geeksforgeeks.org/problems/union-of-two-arrays3538/1
tries: 1
created: 2026-01-29

notes:
i tried to use solve it using just the arrays but it was getting too complicated
so I used hash sets to make it easier
basically we convert both arrays to hash sets to remove duplicates
then the hash set union method is used to find the union of both hash sets, 
this is inbuilt in python which makes it easy
finally we convert the result back to a list and return it

time_complexity: O(n + m) where n = len(a), m = len(b)
space_complexity: O(n) for the hash set storage

edge_cases_tested:
- empty arrays
- arrays of different lengths  
- duplicate elements within arrays
- arrays with overlapping elements

learned:
- using set.union() is cleaner than manual iteration
- converting tohash sets handles duplicates automatically
- list comprehension isn't always needed - sometimes built-in methods are your friend
"""
class Solution:
    def findUnion(self, a, b):
        a_set = set(a)
        b_set = set(b)

        return list(a_set.union(b_set))

if __name__ == "__main__":
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    solution = Solution()
    result = solution.findUnion(a, b)
    print(result)
