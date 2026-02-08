"""
time_spent: 2 minutes (i promise)
difficulty: medium
topic: hash tables, arrays
problem_link: https://leetcode.com/problems/find-players-with-zero-or-one-losses
tries: 1
created: 2026-01-29

notes:
so we are given a 2D array representing matches between players
where each match is represented as [winner, loser]
we need to find players with zero losses and players with one loss
so i was like why don't i use a hash table
initally, i was trying to set some values for each winner and loser
but then i realized we only care about losses, we can just track losses
because the question only asks for players with zero or one loss
so i loop through each match
for each match, i get the winner and loser
i set the winner's losses to 0 if not already present, increment loser's losses by 1
after processing all matches, i have a hash table with player as key and loss count as value
now i need to separate players based on their loss counts
i create two lists, one for zero losses and one for one loss
i loop through the hash table items, and check two conditions
if the loss count is 0, append to zero losses list
if the loss count is 1, append to one loss list
now the question wants us to return the players in increasing order
so i use the sort method on both lists, could've implemented my own sorting algo but nah
most languages have built-in sort methods that are efficient
finally, i return a list containing both lists as per the problem's requirement
that is [zero_losses, one_loss]
sigh... this was a bit tricky but i got it

time_complexity: O(n log n) due to sorting, where n = number of unique players
space_complexity: O(n) for the hash table and the two lists

edge_cases_tested:
- no matches at all
- all players have zero losses
- all players have more than one loss

learned:
- focusing only on required data (loss counts) simplifies the problem
- using hash tables to track counts is very effective
- try to find ways to reduce data tracked to only what's necessary
- all the information you need is in the problem statement
- nothing is in the problem statement that you don't need
"""
from typing import List

class Solution:
    def find_winners(self, matches: List[List[int]]) -> List[List[int]]:
        win_loses = {}

        for match in matches:
            winner, loser = match
            
            # we are only interested in losses, hence we keep wins as 0
            # and increment losses for losers
            win_loses[winner] = win_loses.get(winner, 0)
            win_loses[loser] = win_loses.get(loser, 0) + 1
        
        zero_losses = []
        one_loss = []

        # separate players based on their loss counts
        # we iterate through the hash table items, and check two conditions
        # if the loss count is 0, append to zero losses list
        # the hash table now has player : loss_count pairs
        for player, losses in win_loses.items():
            if losses == 0:
                zero_losses.append(player)
            elif losses == 1:
                one_loss.append(player)

        # the problem asks for sorted lists
        zero_losses.sort() 
        one_loss.sort()

        return [zero_losses, one_loss]


if __name__ == "__main__":
    t = int(input())
    matches = []
    
    for _ in range(t):
        match = list(map(int, input().split()))
        matches.append(match)
    solution = Solution()
    result = solution.find_winners(matches) 
    print(result)
