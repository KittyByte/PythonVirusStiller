from PIL import ImageGrab


def create_screenshot(path_to_save):
    screen = ImageGrab.grab()
    screen.save(path_to_save + '\\screenshot.jpg')
























if __name__ == '__main__':
    create_screenshot(r'C:\Users\Isa\Desktop\Virus2.0\Virus\Targets\System')
