class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        set_nums = set(nums)

        return len(set_nums) != len(nums)