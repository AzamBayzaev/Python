import bisect

def length_of_LIS(nums):
    sub = []
    for x in nums:
        i = bisect.bisect_left(sub, x)
        if i == len(sub):
            sub.append(x)
        else:
            sub[i] = x
    return len(sub)

nums = [10,9,2,5,3,7,101,18]
print(length_of_LIS(nums))  # 4
