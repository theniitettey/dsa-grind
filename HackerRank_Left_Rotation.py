"""
time_spent: 2 minutes (was thinking too much)
difficulty: easy
topic: arrays, implementation
problem_link: https://www.hackerrank.com/challenges/array-left-rotation/problem
tries: 1
created: 2026-02-05

notes:
so we are given an array of integers and a number d
we need to perform d left rotations on the array
a left rotation means that we shift each element of the array to the left by one position
and the first element of the array moves to the end of the array
so for example, if we have an array [1, 2, 3, 4, 5] and 
we perform 2 left rotations, the result would be [3, 4, 5, 1, 2]
to implement this, we can use slicing in Python
but we want to be language-agnostic
so here's the logic i would use:
- i was thinking of simulating the left rotations by looping through the array and shifting elements
but that would be inefficient with a time complexity of O(n * d) since we would be doing d rotations and each rotation would involve shifting n elements
- instead, we can use a more efficient approach by calculating the new positions of the elements after d rotations
- we can create a new array of the same length to store the results
- for each element in the original array, we can calculate its new position using the formula: new_position = (current_position - d) % n
where n is the length of the array
- this way, we can fill the new array in O(n) time since we are just calculating the new positions and placing the elements accordingly
- this approach is more efficient and avoids the need for multiple rotations
can we make this const space complexity?
- we can reverse the first d elements, 
- then reverse the remaining n - d elements, 
- and finally reverse the entire array
- this way, we can achieve the left rotation in-place with O(1) extra space
eg:
original array: [1, 2, 3, 4, 5], d = 2
- reverse first d elements: [2, 1, 3, 4, 5]
- reverse remaining n - d elements: [2, 1, 5, 4, 3]
- reverse entire array: [3, 4, 5, 1, 2]


time_complexity: O(n) where n = length of the array since we loop through the array once to calculate new positions
space_complexity: O(1) since we create a new array to store the results

edge_cases_tested:
- empty array
- d = 0 (no rotations)
- d = n (full rotation, should return the same array)

learned:
- using modular arithmetic to calculate new positions in an array
- in-place array manipulation techniques like reversing segments of the array
"""

from typing import List

class Solution:
    def left_rotation(self, n: int, d: int, arr: List[int]) -> List[int]:
        # 1. New array approach
        # res = [0] * n  # initialize result array with zeros
        # for i in range(n):
        #     new_position = (i - d) % n
        #     res[new_position] = arr[i]
        
        # return res
    
        #2. Const space complexity approach (in-place)
        # we can reverse the first d elements, then reverse the remaining n - d elements, and finally reverse the entire array
        # this way, we can achieve the left rotation in-place with O(1) extra
        for i in range(d // 2):
            arr[i], arr[d - i - 1] = arr[d - i - 1], arr[i]
        
        for i in range(d, (n + d) // 2):
            arr[i], arr[n - (i - d) - 1] = arr[n - (i - d) - 1], arr[i]
        
        for i in range(n // 2):
            arr[i], arr[n - i - 1] = arr[n - i - 1], arr[i]
        
        return arr

        # this has a time complexity of O(n) since we are reversing the array three times
        # and space complexity of O(1) since we are not using any extra space
    

if __name__ == "__main__": 
    n, d = map(int, input().strip().split())
    arr = list(map(int, input().strip().split()))
    solution = Solution()
    result = solution.left_rotation(n, d, arr)
    print(result)

