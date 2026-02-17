"""
time_spent: 5 minutes
difficulty: medium
topic: greedy, arrays, math
problem_link: https://leetcode.com/problems/gas-station/description/
tries: 1
created: 2026-02-15

notes:
so we are given two arrays, one with the amount of gas at each station 
and one with the cost to get to the next station. 
we need to find the starting station index from which we can complete the circuit. 
if there is no such station, we return -1.
when i saw this problem
i was lost intially, becuase i was like, how do we know which station to start from?
and also how can i continually simulate the process of moving from station to station?
then i realized, we actually don't need to simulate the whole process for each station.
so then i came up with the brute force approach, where
we would try starting from each station and see if we can complete the circuit.
this would be O(n^2) in the worst case, which is not efficient.
then i noticed something interesting, the brute force was basically checking if we start from station i, 
can we get to station i+1, then from i+1 to i+2, and so on until we get back to i.
but what was hidden behind my O(n^2) approach was that if we fail at station j, 
then we know that any station between i and j cannot be the starting point, 
because we would have already failed at j when we tried starting from those stations.
so instead of trying every station, we can just jump to station j+1 and try from there.
but why do we jump to j + 1? or when do we know we have to jump to j + 1?
well, if we check our tank at station j and it costs more than what we have in the tank, 
then we know we can't start from any station between i and j, because we would have already failed at j.
so then we can just jump to j + 1 and try from there.
this way, we can find the starting station in O(n) time, because we are essentially skipping over the stations 
that we know can't be the starting point.

time_complexity: O(n) because we are iterating through the stations at most twice (once for the initial check and once for the jump).
space_complexity: O(1) because we are using a constant amount of space to keep track of the current tank and the starting station index.

edge_cases_tested:
- stations with zero gas
- stations where the cost is greater than the gas available

learned:
- sometimes it's really pattern recognition and understanding the problem deeply 
- that leads to an efficient solution, rather than just trying to brute force it.
"""

from typing import List

class Solution:
    def gas_station(self, gas: List[int], cost: List[int]) -> int:
        # you might think we need to track both the total gas and the total cost, 
        # but we actually only need to track the total gas and the current tank.
        total_gas = 0
        current_tank = 0

        # now we need to find the starting station index, we can initialize it to 0
        starting_station = 0
        n = len(gas)

        for i in range(n):
            # we need to find how much gas we have at the current station and how much it costs to get to the next station
            total_gas += gas[i] - cost[i]
            current_tank += gas[i] - cost[i]

            # if we have a negative tank, we can't start from the current starting station
            if current_tank < 0:
                # we need to reset the tank and set the starting station to the next station
                current_tank = 0
                starting_station = i + 1
        
        # at the end of this we need to check two things
        # if the total gas is negative, then we can't complete the circuit, so we return -1
        # since we look ahead, we need to make sure the starting station index is within bounds
        if total_gas < 0 or starting_station >= n:
            return -1
        
        return starting_station


if __name__ == "__main__":
    solution = Solution()
    gas = list(map(int, input().strip().split()))
    cost = list(map(int, input().strip().split()))
    result = solution.gas_station(gas, cost)
    print(result)
