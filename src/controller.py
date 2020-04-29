import time, win32api, win32con, win32gui

VK_CODE = {'left_arrow': 0x25, 'up_arrow': 0x26, 'right_arrow': 0x27, 'down_arrow': 0x28}

def press(*args):
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, 0, 0)
        time.sleep(.05)
        win32api.keybd_event(VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)

def pressAndHold(*args):
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, 0, 0)
        time.sleep(.05)

def pressHoldRelease(*args):
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, 0, 0)
        time.sleep(.05)
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(.1)

def release(*args):
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)

def get_viewport_position():
    left_down, right_up = (), ()

    state_left = win32api.GetKeyState(0x01)
    while not (left_down and right_up):
        a = win32api.GetKeyState(0x01)
        if a != state_left:
            state_left = a
            if a < 0 and not left_down:
                left_down = win32api.GetCursorPos()
            elif a < 0 and not right_up:
                right_up = win32api.GetCursorPos()
        time.sleep(0.001)
    left_up = (left_down[0], right_up[1])
    right_down = (right_up[0], left_down[1])
    return {'left_down': left_down, 'left_up': left_up, 'right_down': right_down, 'right_up': right_up}
