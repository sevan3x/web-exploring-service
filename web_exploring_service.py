import requests
import uuid
import sqlite3
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By


class WebExploringService:
    def __init__(self, main_url, number_of_pages):
        self.main_url = main_url
        self.number_of_pages = number_of_pages

    def check_if_server_is_alive(self):
        res = requests.get(self.main_url, verify=False)

        return res.ok

    def take_screenshots(self):
        screenshots = []

        driver = webdriver.Chrome()

        driver.get(self.main_url)
        screenshots.append(self._take_screenshot(driver))

        html_body = driver.find_element(By.TAG_NAME, "body")
        elements = html_body.find_elements(By.TAG_NAME, 'a')
        links = [e.get_attribute("href") for e in elements]
        filtered_links = [link for link in links if link != self.main_url]

        for n in range(0, self.number_of_pages):
            print(f"Following link: {filtered_links[n]}")
            driver.get(filtered_links[n])
            screenshots.append(self._take_screenshot(driver))
            driver.back()

        self._upload_screenshots_to_db(screenshots)

        driver.quit()

    @staticmethod
    def get_screenshots_by_id(screenshot_id):
        print("Connecting to database...")
        conn = sqlite3.connect('screenshots.db')

        print(f"Searching for a record with id: {screenshot_id}")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM screenshots WHERE id = '{screenshot_id}'")
        screenshots_found = cursor.fetchall()

        conn.close()
        print("Connection closed.")

        return screenshots_found

    @staticmethod
    def _take_screenshot(driver):
        generated_uuid = str(uuid.uuid4().hex)
        screenshot_data = driver.get_screenshot_as_base64()
        taken_at = datetime.timestamp(datetime.utcnow())

        print(f"Screenshot with id: {generated_uuid} has been taken at {taken_at}.")

        return {"id": generated_uuid, "screenshot_data": screenshot_data, "taken_at": taken_at}

    @staticmethod
    def _upload_screenshots_to_db(screenshots):
        print("Connecting to database...")
        conn = sqlite3.connect('screenshots.db')

        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS screenshots
                          (id TEXT PRIMARY KEY, screenshot_data TEXT, taken_at TEXT)''')
        conn.commit()

        print(f"Adding {len(screenshots)} to the table")
        for screenshot in screenshots:
            cursor.execute("INSERT INTO screenshots (id, screenshot_data, taken_at) VALUES (?, ?, ?)",
                           (screenshot["id"], screenshot["screenshot_data"], screenshot["taken_at"]))
        conn.commit()

        conn.close()
        print("Connection closed.")