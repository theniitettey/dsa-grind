"""
time_spent: 2 minute (tbh)
difficulty: easy
topic: arrays, implementation, matrix
problem_link: https://codeforces.com/problemset/problem/263/A
tries: 1
created: 2026-02-05

notes:
so we are given a 5x5 matrix with 24 zeroes and one 1
we need to find the number of moves required to move the 1 to the center
a move consists of swapping the 1 with an adjacent element (up, down, left, right)
to solve this we need to understand a few things first:
what exactly are we doing? yeah... apparently we need to know
at first when i see questions with min, minimum, least etc... they used to scare me
until i really started to think of it this way, you don't need to be utterly greedy
you just need to be greedy enough to find a solution 
look at this diagram below
House 1 --------------------------- House 2 --------------------------- House 3
|                                                                             |
|                                                                             |  
|                                                                             |
|                                                                             |
|                                                                             |  
House 4 --------------------------- House 5 --------------------------- House 6
|                                      |                                      |                                  
|                                      |                                      |
|                                      |                                      |                                     |                                      |                                      |
|                                      |                                      |  
House 7 --------------------------- House 8 --------------------------- House 9
ps: it took a lot of tabs and spaces to make this diagram, but i think it is worth it
if we want to get to house 5 from house 8, we can either to go left, go up and go right
or we can go up, go right and go down or from 8 we should just go up since there is a direct path to 5
the other paths need 3 moves, but the direct path only needs 1 move
so we can see that the minimum number of moves is 1, and we can see that
so really how should you think of min problems?
know your goal state, know your current state, and then find the direct path to the goal state
if you can't find a direct path, eg: graph problems or tree problems where you'll need to explore
you basically just track all the possible ways to reach the goal state and then find the minimum among them
but in this problem, we can easily find the direct path to the goal state
how do we do this? remember the house example, we need to get to house 5 at point (1, 1) -> goal state
and we are at house 8 at point (1, 2) -> current state
so we can just calculate the distance between the current state and the goal state
i.e how many moves can we make to get from the current state to the goal state
or in other words, how many moves can we make in the x-direction and how many moves can we make in the y-direction
or in other words, how many moves can we make up and down and how many moves can we make left and right
so we can just calculate the distance in the x-direction and the distance in the y-direction and
then add them together to get the total number of moves required to get to the goal state
so for the house example x distances are 1, 1 and y are  1, 2
so x-move = 1 - 1 = 0 and y-moves = 1 - 2 = -1, but one thing, moves are absolute, always positive
so we need to take the absolute value of the moves, so x-move = abs(1 - 1) = 0 and y-move = abs(1 - 2) = 1
so total moves = x-move + y-move = 0 + 1 = 1, and from the visual example and the calculation, 
we can see that the answer is correct, they're both 1, so we can just apply this logic to the problem
except with a little twist... for the house problem, we know our current state beforehand
but in this problem, we don't know our current state, we need to find it first
however we know what our goal state is, we need to get to the center of the matrix at point (2, 2)
so we can just iterate through the matrix to find the current state first
then we can calculate the distance from the current state to the goal state and return that as the answer
and how do we know our current state? in a matrix of 0's and 1's we want to move the 1 to the center,
so it's basically asking, where is 1 located in the matrix? find it? and
then calculate the distance from that location to the center of the matrix
i know this is a very long explanation, but i just wanted to explain my thought process 
and how i arrived at the solution


edge_cases_tested:
- when the 1 is already in the center, the answer should be 0
- not in the question, but what if there is no 1 in the matrix
- or what if there are multiple 1's in the matrix, but this is not possible according to the problem statement, 
- so we can ignore this case 

learned:
- how to approach min problems, know your goal state, 
- know your current state, and 
- find the direct path to the goal state or 
- track all the possible ways to reach the goal state and then find the minimum among them
"""

from typing import List

class Solution:
    def beautiful_matrix(self, matrix: List[List[int]]) -> int:
        # intialize default values for current state and goal state
        # 0, 0 because we haven't found the 1 yet, 
        # and we can just use any value for the goal state since we know it is at (2, 2)
        x, y = 0, 0
        x_goal, y_goal = 2, 2

        # find the current state (position of the 1 in the matrix)
        # i want to be a really greedy competitive programmer,
        # the break statement is useful but has one problem
        # it breaks just the inner loop, but we want to break out of both loops once we find the 1
        # we could use a flag variable to indicate that we found the 1 and then break out of the outer loop as well
        # or we could wrap it in a function and return the current state once we find the 1, 
        # but for simplicity, we can just use a flag variable
        # for i in range(5):
        #     for j in range(5):
        #         if matrix[i][j] == 1:
        #             # found it, update the current state and break out of the loop
        #             x, y = i, j
        #             break

        # function with return statement to break out of both loops once we find the 1
        # def find_current_state(matrix):
        #     for i in range(5):
        #         for j in range(5):
        #             if matrix[i][j] == 1:
        #                 return i, j
        #     return 0, 0 # default value if we don't find the 1, but this should never happen according to the problem statement
        
        # then we can get the current state by calling the function
        # x, y = find_current_state(matrix)

        found = False
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == 1:
                    # found it, update the current state and break out of the loop
                    x, y = i, j
                    found = True
                    break
            if found:
                break

        # calculate the Manhattan distance from current position to goal position
        # basically, how many moves in all directions do we need to make to get from current state to goal state
        return abs(x - x_goal) + abs(y - y_goal)

if __name__ == "__main__":
    solution = Solution()
    grid = []
    for _ in range(5):
        row = list(map(int, input().strip().split()))
        grid.append(row)
    result = solution.beautiful_matrix(grid)
    print(result)