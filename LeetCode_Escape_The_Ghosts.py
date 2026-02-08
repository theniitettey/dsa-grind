"""
time_spent: 5 minutes (was a tricky one)
difficulty: medium
topic: arrays, math, geometry
problem_link: https://leetcode.com/problems/escape-the-ghosts/
tries: 1
created: 2026-02-08

notes:
so basically we are playing PACMAN, just in arrays and grids... sigh
so the input is a list of ghost positions and a target position
we need to determine if we can reach the target before any of the ghosts can reach us
there are some caveats though,
we start at the position (0, 0) and we can move in four directions: up, down, left, right
we can only move one unit at a time
the ghosts can also move in the same way as us, one unit at a time in four directions
initially i was trying to simulate the movement of the ghosts and us, 
but that would be very inefficient and complicated
you need to understand game theory for that, and it would be a nightmare to implement
you can try though, as a fun exercise, but it's not the optimal solution
the optimal solution is actually quite simple,
if i'm at positon (0, 0) and i want to reach the target (x, y),
the minimum number of steps i need to take is the Manhattan distance between (0, 0) and (x, y)
the Manhattan distance is calculated as abs(x - 0) + abs(y - 0)
i bet you've seen this before, it's a common distance metric in grid problems
now for the ghosts, we need to calculate the Manhattan distance from each ghost's position to the target
now since we now know the minimum steps for us to reach the target
we want to figure out who'd reach the target first, us or the ghosts
in escence we just need to see if the ghost can get to us before we get to the target
if the ghost can reach the target in less than or equal to the steps we need, 
then we can't escape, because the ghost can just wait at the target and catch us when we arrive
otherwise, if all the ghosts need more steps to reach the target than we do, then we can escape
so we just need to compare the steps we need with the steps each ghost needs,
if any ghost can reach the target in less than or equal to our steps, we return False
otherwise, we return True

time_complexity: O(n) where n is the number of ghosts, because we need to calculate the distance for each ghost
space_complexity: O(1) because we are using a constant amount of space to store the steps and compare them

edge_cases_tested:
- if there are no ghosts, we can always escape, so the result should be True
- if the target is at (0, 0), we are already at the target, so we can escape, the result should be True
- if a ghost is already at the target, we can't escape, the result should be False

learned:
- sometimes you don't need to simulate the entire proces
- try to think, "do i really need to simulate this, or is there a mathematical way to determine the outcome?"
- we might need some school knowledge after all, listen to your teachers, they know what they're doing
"""

from typing import List

class Solution:
    def escape_ghosts(self, ghosts: List[List[int]], target: List[int]) -> bool:
        target_x, target_y = target
        steps_needed = abs(target_x) + abs(target_y)

        n = len(ghosts)
        
        for i in range(n):
            ghost_x, ghost_y = ghosts[i]
            ghost_steps = abs(ghost_x - target_x) + abs(ghost_y - target_y)

            if ghost_steps <= steps_needed:
                return False    
    
        return True
        

if __name__ == "__main__":
    solution = Solution()
    target = list(map(int, input().strip().split()))
    n = int(input().strip())
    ghosts = []
    for _ in range(n):
        ghost = list(map(int, input().strip().split()))
        ghosts.append(ghost)
    result = solution.escape_ghosts(ghosts, target)
    print(result)
