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
    first_click, second_click = (), ()

    state_left = win32api.GetKeyState(0x01)
    while not (first_click and second_click):
        a = win32api.GetKeyState(0x01)
        if a != state_left:
            state_left = a
            if a < 0 and not first_click:
                first_click = win32api.GetCursorPos()
            elif a < 0 and not second_click:
                second_click = win32api.GetCursorPos()
        time.sleep(0.001)

    return [min([first_click[0], second_click[0]]),
            min([first_click[1], second_click[1]]),
            max([first_click[0], second_click[0]]),
            max([first_click[1], second_click[1]])]
