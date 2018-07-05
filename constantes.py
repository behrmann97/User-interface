import wx

app = wx.App(False)
SCREEN_WIDTH, SCREEN_HEIGHT = wx.GetDisplaySize()

while_creator = (50, 30)
if_creator = (50, 130)
else_creator = (50, 230)
set_creator = (50, 230)
first_next = (400, 55)

def adjust(nums):
    if len(nums) == 1:
        return nums[0] * SCREEN_WIDTH/1536
    if len(nums) == 2:
        return nums[0] * SCREEN_WIDTH/1536, nums[1] * SCREEN_HEIGHT/864
    else:
        return adjust(nums[0:2]) + adjust(nums[2:4])
