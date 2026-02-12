"""
time_spent: 1 minute
difficulty: easy
topic: sorting, greedy, arrays
problem_link: https://leetcode.com/problems/minimum-number-of-moves-to-seat-everyone
tries: 1
created: 2026-02-12

notes:
so there are n available seats and n students standing
we are given two arrays, one for the seats and one for the students
seats[i] is the position of the ith seat and students[j] is the position of the jth student
a move consists of incrementing or decrementing the position of the ith student by 1
we want to find the minimum number of moves required to move each student to a seat
such that no two students are in the same seat
so hmmm... one thing i noticed is we basically have to be greedy
but what exactly does being greedy mean in DSA?
greedy means making the locally optimal choice at each step with the hope of finding a global optimum
buzz words... i know
it just means, we want to maximize our chances of finding the best solution by making the best choice at each step
so bring that here, we want to minimize the number of moves,
so we want to minimize the distance between each student and their assigned seat
how can we do this? well, what if we sort both the seats and the students arrays?
if we sort both arrays, then we can pair the smallest seat with the smallest student, 
the second smallest seat with the second smallest student, and so on
this way, we are minimizing the distance between each student and their assigned seat
so we can sort both arrays and then calculate the total number of moves by summing 
the differences between the corresponding elements of the two arrays, absolute value of course
this should give us the minimum number of moves required to seat everyone

time_complexity: O(n log n) due to sorting both arrays
space_complexity: O(1) if we sort in place, otherwise O(n) if we use extra space for sorting

edge_cases_tested:
- n = 1, where there is only one seat and one student

learned:
- the importance of sorting in greedy algorithms to find optimal solutions
- we can minimize distances by sorting both arrays and pairing elements in order
"""

from typing import List

class Solution:
    def minimum_number_of_moves_to_seat_everyone(self, seats: list[int], students: list[int]) -> int:
        # sort both arrays
        # .sort() is in-place
        # so no extra space is used for sorting
        seats.sort()
        students.sort()
        
        moves = 0
        n = len(seats)

        for i in range(n):
            moves += abs(seats[i] - students[i])

        return moves



if __name__ == "__main__":
    solution = Solution()
    seats = list(map(int, input().strip().split()))
    students = list(map(int, input().strip().split()))
    result = solution.minimum_number_of_moves_to_seat_everyone(seats, students)
    print(result)
