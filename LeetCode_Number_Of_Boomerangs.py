"""
time_spent: 5 minutes (was a tough one)
difficulty: medium
topic: hash tables, math, implementation
problem_link: https://leetcode.com/problems/number-of-boomerangs/description/
tries: 1
created: 2026-07-02

notes:
so we are given a list of points, and we need to find the number of boomerangs. 
a boomerang is a tuple of points (i, j, k) such that the 
distance between i and j is equal to the distance between i and k. 
we can use a hash table to count the number of points that are at the same distance from each point. 
for each point, we can calculate the distance to every other point and store the count in the hash table. 
then, for each distance, we can calculate the number of boomerangs using the formula n * (n - 1), 
n * (n - 1) because, we need ordered pairs, and they must be unique, basically 2 unique points
so therefore, if i have n choices for the first point, i have one less choice (n - 1) for the second point,
now the total number of ordered pairs (boomerangs) for that distance is n * (n - 1),
this is also  known as a permutation, because we care about order
where n is the count of points at that distance.
now when we say distance, we can use the squared distance to avoid floating point issues.
i tried to use the manhattan distance at first, 
but it didn't work because the problem is based on the Euclidean distance.
so we pick a point "a" as the center
create a dist hash table to count the number of points at each distance from the center
we pick another point "b" and calculate the distance from "a" to "b", and increment the count in the dist hash table
think of if it like b <---some distance---> a <---some distance---> c
if the distance from a to b is the same as the distance from a to c, then we have a boomerang (a, b, c) and (a, c, b)
basically we hope to find a c later in the future for that distance
after we've populate the dist hash table for a, 
we can calculate the number of boomerangs for each distance using the formula n * (n - 1), 
where n is the count of points at that distance, where n is just the dist hash table values.
sigh... this question really made me think a lot about the implementation and the math behind it,
ps: they are permutations, euclidean distance, manhattan distance, and squared distance


time_complexity: O(n^2) - we have to calculate the distance from each point to every other point, which takes O(n) time for each of the n points.
space_complexity: O(n) - we use a hash table to store the count of points at each distance, which can have at most n entries in the worst case (when all points are at different distances from the center point).

edge_cases_tested:
- empty list of points
- list of points with only one point

learned:
- it's not always going to be just DSA sometimes, sometimes it's DSA plus math/geometry/implementation
- be careful with distance calculations, use squared distance to avoid floating point issues
"""

from typing import List

class Solution:
    def number_of_boomerangs(self, points: List[List[int]]):
        boomerangs = 0
        n = len(points)

        # iterate through each point as the center
        for i in range(n):
            dist = {}
            point_a = points[i]
            # calculate the distance from the center point to every other point
            for j in range(n):
                # we skip the same point
                # not really necessary since the distance from a point to itself is 0, but we can just skip it to avoid unnecessary calculations
                if i == j:
                    continue
                point_b = points[j]
                d = (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2
                
                if d not in dist:
                    dist[d] = 0
                dist[d] += 1
            
            # calculate the number of boomerangs for each distance
            for count in dist.values():
                boomerangs += count * (count - 1)
        
        return boomerangs
        


if __name__ == "__main__":
    solution = Solution()
    t = int(input().strip())
    points = []
    for _ in range(t):
        point = list(map(int, input().strip().split()))
        points.append(point)
    result = solution.number_of_boomerangs(points)
    print(result)
