import logging
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class Player:
    def __init__(self):
        self.name = "Player"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def go2(self, link: str) -> None:
        """
        drives the chrome to the link passed
        :param link: url for player to go
        :return: Nothing to return
        """
        self.driver.get(link)

    def form_submit(self, button_id: str, wait_time: int) -> None:
        """
        clicks on the form button with provided id
        :param button_id: id of the html tag
        :param wait_time: how long the player should wait after submitting the form
        :return: nothing
        """
        logging.info(f"{self.name}:click_button")
        try:
            form_button_element = self.driver.find_element(by=By.ID, value=button_id)
            form_button_element.click()
            time.sleep(wait_time)
        except Exception as e:
            logging.error(f"something went wrong while clicking the submit button: {e}")
        return

    def form_selector(self, element_tag: str, attribute_name: str, attribute_value: str, wait_time: int) -> None:
        """
        selects the item on the form with the element tag, which the attribute name and value
        :param element_tag: html tags like div, li
        :param attribute_name: tag attributes like 'data-class'
        :param attribute_value: tag attribute values like 'soAD'
        :param wait_time: time to wait in seconds after selection
        :return: nothing
        """
        logging.info(f"{self.name}:form_selector_and_click")
        try:
            form_button_element = self.driver.find_element(
                by=By.XPATH,
                value=f"//{element_tag}[contains(@{attribute_name}, '{attribute_value}')]"
            )
            form_button_element.click()
            time.sleep(wait_time)
        except Exception as e:
            logging.error(f"something went wrong while selecting the value in form: {e}")
        return

    def form_set_and_click(self, element_id: str, button_id: str, value: str, wait_time: int = 1) -> None:
        """
        finds the html element by id, and enters the provided value, and clicks on the button and waits for a seconds
        :param element_id: id of the form input tag of the form element
        :param button_id: id of the form submit button tag of the form element
        :param value: value to be set for the form element
        :param wait_time: optional value to set the wait/sleep time after clicking the button
        :return: Nothing to return
        """
        logging.info(f"{self.name}:form_set_and_click")
        try:
            form_email_element = self.driver.find_element(by=By.ID, value=element_id)
            form_email_element.send_keys(value)
        except Exception as e:
            logging.error(f"something went wrong while entering the value to input tag: {e}")
        self.form_submit(button_id=button_id, wait_time=wait_time)
        return


def main():
    player = Player()
    player.go2(f"{os.environ['CITRIX_URL']}")
    time.sleep(5)
    player.form_set_and_click(
        element_id="i0116",
        button_id="idSIButton9",
        value=f"{os.environ['CITRIX_USERNAME']}",
        wait_time=2
    )
    player.form_set_and_click(
        element_id="i0118",
        button_id="idSIButton9",
        value=f"{os.environ['CITRIX_PASSWORD']}",
        wait_time=2
    )
    player.form_selector(
        element_tag='div',
        attribute_name='data-value',
        attribute_value='TwoWayVoiceMobile',
        wait_time=20)
    player.form_selector(
        element_tag='button',
        attribute_name='data-testid',
        attribute_value='detection-detect_workspace',
        wait_time=1
    )
    done = input()
    while done != "done":
        pass


if __name__ == "__main__":
    main()
