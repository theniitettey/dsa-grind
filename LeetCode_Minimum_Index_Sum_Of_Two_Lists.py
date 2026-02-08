"""
time_spent: 3 minutes (this was a tough one)
difficulty: easy
topic: arrays, hash tables, strings
problem_link: https://leetcode.com/problems/minimum-index-sum-of-two-lists/
tries: 1
created: 2026-02-08

notes:
so we are given two list of strings, list1 and list2
we need to find the common strings between the two lists with the least index sum \
least index sum = (index in list1 + index in list2)
if there are multiple common strings with the same least index sum, we need to return all of them
so we can use bruteforce for start
we pick a string from list1 and check if it is in list2
if it is we calculate the index sum and keep track of the minimum index sum and the corresponding strings
if we find a string with a smaller index sum, we update our minimum index sum and reset our result list
if we find a string with the same index sum, we add it to our result list
this approach has a time complexity of O(n*m) where n and m are the lengths of list1 and list2 respectively
we can optimize this by using a hash table, i thought of two ways for this
which my first approach, i create a hash table for list1 where the key is the string and the value is its index
then we iterate through list2 and for each string, we check if it is in the hash table
then i add the index from list2 and the index from the hash table to get the index sum
and we keep track of the minimum index sum and the corresponding strings as before
after i'm done, i iterate through the hash table in key value pairs
and i check if the index sum for each string is equal to the minimum index sum
if it is, i add it to the result list
but there was one problem with this approach, 
it was still appending all the strings with the same index sum to the result list, 
even if they were not common strings
so i added an extra check, a flag
so in the first loop, where we populate the hash table
instead of storing string : index, we store string : (index, flag), the flag is initially set to False
then in the second loop, comparing the strings from list2 with the hash table, 
if we find a match, we set the flag to True and calculate the new index, prev_index + current_index
then we store (index_sum, flag) in the hash table
now in the key value pair loop,
we check if the flag is True and if the index sum is equal to the minimum index sum
if both conditions are satisfied, we add the string to the result list
this way we ensure that we only add common strings to the result list
however i got another realization, do we really need a flag or a key value pair loop at the end?
and the answer was no, we keep thesame hash table structure, but instead of storing (index, flag),
and we set the minimum index sum to a very large number 
we can store just the index in the hash table, that's for the first loop
now in the second loop, when we find a match, 
we calculate the index sum and compare it with the minimum index sum like this:
- if the index sum < minimum index sum, 
we update the minimum index sum and reset the result list with the current string
- if the index sum == minimum index sum,
we add the current string to the result list
we don't need to check the flag or do a separate loop at the end, 
because we are only adding common strings to the result list in the second loop
and this worked perfectly, it was much cleaner and more efficient than the previous approach


time_complexity: O(n + m) where n and m are the lengths of list1 and list2 respectively
space_complexity: O(n) where n is the length of list1
                  because we are storing the strings and their indices in a hash table

edge_cases_tested:
- if one of the lists is empty, the result should be an empty list
- if there are no common strings, the result should be an empty list

learned:
- a flag can be useful to keep track of certain conditions, 
- but sometimes we can avoid it by structuring our data differently
- sometimes you just need to reset your answer when you find a better solution
- instead of trying to keep track of all the possibilities

"""

from typing import List

class Solution:
    # for some reason, leetcode named the function find_resturant instead of minimum_index_sum_of_two_lists,
    def find_restaurant(self, list1: List[str], list2: List[str]) -> List[str | None]:
        # 1. Brute force approach
        min_index_sum = float('inf')
        result = []
        n = len(list1)
        m = len(list2)

        # # loop through list1 and list2 to find common strings and calculate index sums
        # for i in range(n):
        #     for j in range(m):
        #         if list1[i] == list2[j]:
        #             index_sum = i + j
        #             if index_sum < min_index_sum:
        #                 min_index_sum = index_sum
        #                 result = [list1[i]]
        #             elif index_sum == min_index_sum:
        #                 result.append(list1[i])
        # return result

        # this approach has a time complexity of O(n*m) where n and m are the lengths of list1 and list2 respectively

        # 2. hash table with flag approach
        # common_strings = {}

        # # populate the hash table with list1
        # for i in range(n):
        #     string = list1[i]
        #     common_strings[string] = (i, False)  # store index and flag

        # # compare list2 with the hash table
        # for j in range(m):
        #     string = list2[j]
        #     if string in common_strings:
        #         prev_index, flag = common_strings[string]
        #         index_sum = prev_index + j
        #         min_index_sum = min(min_index_sum, index_sum)  # update minimum index sum
        #         flag = True  # set flag to True since we found a common string
        #         common_strings[string] = (index_sum, flag)  # update with index sum and set flag to True

        # # iterate hash table in key value pairs to find strings with minimum index sum and flag True
        # for key, value in common_strings.items():
        #     index_sum, flag = value
        #     if flag and index_sum == min_index_sum:
        #         result.append(key)

        # return result

        # this approach has a time complexity of O(n + m) where n and m are the lengths of list1 and list2 respectively
        # but it's not pure O(n + m) because we have to iterate through the hash table at the end, which can be O(n) in the worst case
        # so it's actually O(n + m + n) = O(2n + m) = O(n + m) because we drop the constant factor

        # 3. Optimized hash table approach without flag
        common_strings = {}

        # populate the hash table with list1
        for i in range(n):
            string = list1[i]
            common_strings[string] = i  # store index
        
        # compare list2 with the hash table
        for j in range(m):
            string = list2[j]
            if string in common_strings:
                prev_index = common_strings[string]
                index_sum = prev_index + j
                if index_sum < min_index_sum:
                    min_index_sum = index_sum # update minimum index sum
                    result = [string]  # reset result list with current string
                elif index_sum == min_index_sum:
                    result.append(string)  # add current string to result list

        return result

        # this approach has a time complexity of O(n + m) where n and m are the lengths of list1 and list2 respectively
        


if __name__ == "__main__":
    solution = Solution()
    n, m = map(int, input().split())
    list1 = []
    for _ in range(n):
        list1.append(input())
    list2 = []
    for _ in range(m):
        list2.append(input())
    result = solution.find_restaurant(list1, list2)
    print(result)
