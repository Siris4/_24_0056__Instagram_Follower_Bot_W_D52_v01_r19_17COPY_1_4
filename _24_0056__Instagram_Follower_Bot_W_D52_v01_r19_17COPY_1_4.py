import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Constants
INSTAGRAM_EMAIL = "YOUR_EMAIL"
INSTAGRAM_PASSWORD = "YOUR_PASSWORD"
SIMILAR_ACCOUNT = "billnye"

class InstaFollower:
    URL_FOR_INSTAGRAM = "https://www.instagram.com/"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.init_driver()

    def init_driver(self):
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{timestamp} - {message}")

    def login(self):
        start_timer = time.time()
        self.log_message("Starting login process")
        self.driver.get(self.URL_FOR_INSTAGRAM)
        time.sleep(5)

        username_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys(self.username)
        self.log_message("Username/email entered")

        password_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(self.password)
        self.log_message("Password entered")

        password_field.send_keys(Keys.RETURN)
        self.log_message("Login submitted")
        time.sleep(5)

        self.click_not_now_buttons()
        self.search_and_select_account(SIMILAR_ACCOUNT)
        self.click_on_followers()
        self.follow_users()

        end_timer = time.time()
        total_login_time = end_timer - start_timer
        self.log_message(f"Total login time: {total_login_time} seconds")
        return total_login_time

    def click_not_now_buttons(self):
        not_now_selectors = [
            {"by": By.XPATH, "value": "//button[text()='Not Now'] | //div[text()='Not now']"},
            {"by": By.CSS_SELECTOR, "value": "button._a9--._ap36._a9_1"},
            {"by": By.CLASS_NAME, "value": "_a9--"}
        ]

        for selector in not_now_selectors:
            try:
                not_now_button = WebDriverWait(self.driver, 4).until(
                    EC.element_to_be_clickable((selector["by"], selector["value"])))
                not_now_button.click()
                self.log_message(f"'Not now' button clicked using {selector['by']}='{selector['value']}'")
                time.sleep(1)  # brief pause between clicks
            except TimeoutException:
                self.log_message(f"No 'not now' button appeared using {selector['by']}='{selector['value']}' within the timeout period.")
                continue  # Skip to the next selector if the current one is not found

    def search_and_select_account(self, account_name):
        self.log_message(f"Searching for account {account_name}")

        def attempt_select_account():
            search_button_found = False
            search_button_selectors = [
                {"by": By.CSS_SELECTOR, "value": "svg[aria-label='Search']"},
                {"by": By.XPATH, "value": "//svg[@aria-label='Search']"},
                {"by": By.CSS_SELECTOR,
                 "value": "#mount_0_0_Fc > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1.x1dr59a3.xixxii4.x13vifvy.xeq5yr9.x1n327nk > div > div > div > div > div.x1iyjqo2.xh8yej3 > div:nth-child(2) > span > div > a > div > div:nth-child(1) > div > div > svg"}
            ]
            for selector in search_button_selectors:
                try:
                    search_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((selector["by"], selector["value"])))
                    search_button.click()
                    search_button_found = True
                    self.log_message(f"Search button clicked using {selector['by']}='{selector['value']}'")
                    break
                except TimeoutException:
                    self.log_message(f"Search button not found using {selector['by']}='{selector['value']}'")

            if not search_button_found:
                self.log_message("Failed to find and click the search button.")
                return False

            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
            search_input.clear()
            search_input.send_keys(account_name)
            search_input.send_keys(Keys.RETURN)
            time.sleep(2)  # Wait for search results to load

            # Now specifically targeting the second profile in the search results
            top_account_selector = f"(//span[contains(text(), '{account_name}')])[2]"

            try:
                top_account = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, top_account_selector)))
                top_account.click()
                self.log_message(f"Second account clicked using {top_account_selector}")
                return True
            except TimeoutException:
                self.log_message(f"Second account not found using {top_account_selector}")
                return False

        # First attempt
        if attempt_select_account():
            return

        # Second attempt
        self.log_message("Retrying search and select account.")
        attempt_select_account()

    def click_on_followers(self):
        followers_link_selector = "//a[contains(@href, '/followers/')]"
        try:
            followers_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, followers_link_selector)))
            followers_link.click()
            self.log_message("Clicked on 'Followers' link")
        except TimeoutException:
            self.log_message("Followers link not found within the timeout period")

    def follow_users(self):
        scroll_attempts = 0
        max_scroll_attempts = 10  # Increase the scroll attempts to ensure we cover more ground if needed

        while scroll_attempts < max_scroll_attempts:
            # Use a more specific selector that targets the "Follow" button
            # Adjust the selector as per the provided HTML structure
            follow_buttons = self.driver.find_elements(By.XPATH, "//div[contains(@class, '_aade') and text()='Follow']")

            if not follow_buttons:
                scroll_attempts += 1
                self.driver.execute_script("window.scrollBy(0, 500);")  # Adjust scroll value as needed
                time.sleep(2)  # Wait for new buttons to appear
                continue

            for button in follow_buttons:
                try:
                    # Scroll the button into view
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(1)  # Brief pause to ensure button is in view

                    # Click the button
                    button.click()
                    self.log_message("Clicked a 'Follow' button")
                    time.sleep(1)  # pause between following actions

                except Exception as e:
                    self.log_message(f"Failed to click 'Follow' button: {e}")
                    continue  # Try next button if the current one fails

            scroll_attempts += 1  # Increment scroll attempts after each full pass

            # Brief pause before the next scroll to allow for loading
            time.sleep(1)

    def close_browser(self):
        input("Press Enter to close the browser...")
        self.driver.quit()
        self.log_message("Browser closed.")

# Instantiate and use the Instagram bot
instagram_bot = InstaFollower(INSTAGRAM_EMAIL, INSTAGRAM_PASSWORD)
total_login_time = instagram_bot.login()
print(f"Total login time: {total_login_time} seconds")
instagram_bot.click_on_followers()
instagram_bot.follow_users()
instagram_bot.close_browser()
