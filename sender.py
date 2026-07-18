import pyautogui as pg
import pyperclip as pp
import time
from PIL import ImageGrab


class SendPersonalizedMessage:
    def __init__(self, sender="whatsapp"):
        self.senders = {
            "whatsapp": self.whatsapp_sender,
            "email": self.email_sender,
            "sms": self.sms_sender,
            "instagram": self.instagram_sender,
        }

        try:
            self.sender = self.senders[sender]
        except KeyError:
            raise ValueError(f"Canal '{sender}' não suportado.")

    def send(self, *args, **kwargs):
        return self.sender(*args, **kwargs)

    def whatsapp_sender(self, cellphone, message, name=None):
        url = f'https://wa.me//55{cellphone}?text={message}'.replace(' ', '%20').replace('\n', '%0A')
        print(url)
        pp.copy(url)
        pg.hotkey('alt', 'tab')
        time.sleep(2)
        pg.hotkey('ctrl', 'n')
        time.sleep(2)
        pg.hotkey('ctrl', 'v')
        time.sleep(2)
        pg.press('enter')
        time.sleep(2)

        self.screenshot_cut(name)

        pg.press('enter')
        time.sleep(2)
        pg.press('escape')
        pg.hotkey('alt', 'tab')
        time.sleep(2)
        pg.hotkey('alt', 'f4')

    def screenshot_cut(self, name):
        # Descobre o tamanho da tela
        screen  = ImageGrab.grab()
        screen_width, screen_height = screen.size

        # Região central ocupando 50% da largura e 50% da altura
        crop_width = screen_width // 3
        crop_height = screen_height // 3

        left = (screen_width - crop_width) // 2
        top = (screen_height - crop_height) // 3
        right = left + crop_width
        bottom = top + crop_height

        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        screenshot.save(f"{name}.png")


    def email_sender(self):
        ...

    def sms_sender(self):
        ...

    def instagram_sender(self):
        ...