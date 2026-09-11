import pyautogui


class Controller:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    def move_cursor(self, x, y):

        screen_x = int(x * self.screen_width)
        screen_y = int(y * self.screen_height)

        pyautogui.moveTo(screen_x, screen_y)

    def click(self):
        pyautogui.click()

    def scroll(self, direction, amount=200):

        if direction == "up":
            pyautogui.scroll(amount)

        elif direction == "down":
            pyautogui.scroll(-amount)