from typing import Union

from playwright.sync_api import Browser, Page


class BrowseTheWeb:
    """
    Gives an actor the ability to use a playwright browser

    playwright = sync_playwright().start()
    don = Actor("Don")
    don.add_ability(BrowseTheWeb.using_chromium(playwright))
    page = don.get_ability(BrowseTheWeb).current_page
    """

    def __init__(self, browser: Browser) -> None:
        self.browser = browser
        self.current_page: Union[Page, None] = None
        self.pages = []

    @staticmethod
    def using(browser: Browser) -> "BrowseTheWeb":
        return BrowseTheWeb(browser)

    @staticmethod
    def using_firefox(playwright) -> "BrowseTheWeb":
        browser = playwright.firefox.launch()
        return BrowseTheWeb(browser)

    @staticmethod
    def using_chromium(playwright) -> "BrowseTheWeb":
        browser = playwright.chromium.launch()
        return BrowseTheWeb(browser)

    def forget(self) -> None:
        self.browser.close()
        self.pages = []
        self.current_page = None

    def __repr__(self):
        return self.__class__.__name__
