from time import sleep, time
from typing import List
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement


class MyChrome(Chrome):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.parametros_inicializacao()
        # self.go_home()
        # self.default_window_size()

    def parametros_inicializacao(self):
        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
            """
        })
        self.execute_cdp_cmd("Network.enable", {})
        self.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
                             "headers": {"User-Agent": "browser1"}})

    def quit_driver(self):
        self.close()
        self.quit()

    def mude_para_aba(self, index):
        """
        Muda para a aba com indece == index
        """
        self.switch_to.window(self.window_handles[index])

    def go_home(self):
        self.get('https://www.bet365.com/#/IP/B1')

    def get_initial_page(self, pagina):
        if self.current_url == pagina:
            pass
        else:
            self.get(pagina)

    def default_window_size(self):
        self.set_window_size(1280, 720)

    def retorne_quando_encontrar(self, find_by,
                                 value,
                                 timeout=2) -> List[WebElement]:

        delta_time = 0.2
        expire_time = time() + timeout
        while time() < expire_time:
            e = self.find_elements(by=find_by, value=value)
            if e:
                return e
            else:
                sleep(delta_time)

        return []


def MyChrome_configurado(cookies=None) -> MyChrome:
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--mute-audio")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    options.add_argument('--disable-gpu')
    options.add_experimental_option('useAutomationExtension', False)

    driver = MyChrome(options=options)
    if cookies is not None:
        for cookie in cookies:
            driver.add_cookie(cookie)
    return driver
