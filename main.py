from navegador import MyChrome_configurado, MyChrome
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from typing import List, Text, Union
import json


def get_matchCentreData(driver: MyChrome, url: int) -> Union[dict, bool]:
    driver.get(url)
    sleep(10)
    try:
        return driver.execute_script('return matchCentreData')
    except JavascriptException:
        return False


def get_links_with_match_report(driver: MyChrome) -> List[Text]:
    class_match_report = 'match-link'
    sleep(5)
    elements: List[WebElement] = driver.find_elements_by_class_name(
        class_match_report)
    return [ele.get_attribute('href') for ele in elements]


def click_previus_day(driver: MyChrome) -> None:
    class_btn = 'ui-icon-triangle-1-w'
    btn: Union[WebElement, None] = driver.find_element_by_class_name(class_btn)
    if btn:
        btn.click()


def main():
    driver1 = MyChrome_configurado()
    driver2 = MyChrome_configurado()
    driver1.get('https://1xbet.whoscored.com/LiveScores')
    sleep(5)
    click_previus_day(driver1)

    while True:
        match_urls = get_links_with_match_report(driver1)
        for url in match_urls:
            driver2.get('chrome://newtab')
            var = get_matchCentreData(driver2,
                                      url.replace('MatchReport', 'Live'))
            Id = url.split('/')[4]
            if var:
                with open(f"data/{Id}.json", mode='w') as f:
                    json.dump(var, f)
        click_previus_day(driver1)


if __name__ == "__main__":
    main()
