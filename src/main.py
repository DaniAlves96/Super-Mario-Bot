import controller
import image_processing

if __name__ == '__main__':
    #controller.pressHoldRelease('left_arrow', 'up_arrow', 'left_arrow')
    print("Left click 2 times to get viewport")
    viewport = controller.get_viewport_position()
    image_processing.screen_record([150, 120, 1300, 800])