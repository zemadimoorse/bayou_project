from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawl_document import crawl_for_links, crawl_for_billing
from crawl_json import filter_driver_requests, crawl_json_for_billing
from interfaces_pb2 import UserCredentials

# --- Configure Chrome to run in headless mode ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")  # Helps avoid layout issues in headless

# --- Credentials and login element identifiers.  ---
# If using another utility when running locally, change these values.
USERNAME = "" # Add username here.
PASSWORD = "" # Add password here.
UTILITY_ROOT_URL = "https://pse.com/login"
BILLING_URL_SUFFIX_FOR_TESTING = "/account-and-billing/my-bill"
# An alternative is to use an LLM to parse the root landing page and determine login element selectors.
USERNAME_INPUT_ID = "Username"
PASSWORD_INPUT_ID = "Password"
LOGIN_BUTTON_ID = "signin-btn"

def build_credentials():
    user = UserCredentials()
    user.username = USERNAME
    user.password = PASSWORD
    user.root_url = UTILITY_ROOT_URL
    user.login_button_id = LOGIN_BUTTON_ID
    user.username_input_id = USERNAME_INPUT_ID
    user.password_input_id = PASSWORD_INPUT_ID

    return user

# TODO: Add async handling.
def parse_data(user: UserCredentials):
    # TODO: replace with an error.
    if not user: 
        return

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to the stored login page
        driver.get(user.root_url)

        # Find login fields and fetch login input elements. 
        # NOTE: In prod, we would want to wait for a page state change instead of a timeout. Applies throughout.
        wait = WebDriverWait(driver, 20)  # Wait for up to 20 seconds
        username_input = wait.until(EC.presence_of_element_located((By.ID, user.username_input_id)))
        password_input = driver.find_element(By.ID, user.password_input_id)

        # Enter credentials
        username_input.send_keys(user.username)
        password_input.send_keys(user.password)

        # Locate and click the login button
        login_button = driver.find_element(By.ID, user.login_button_id)
        login_button.click()

        print("Login submitted. Waiting for next page to load...")
        wait = WebDriverWait(driver, 20)

        print("Crawling and classifying links...")
        # Step 1: evaluate page links and classify them for navigation.
        # In prod, we would want caching to avoid repeated calls.
        parsed_links = crawl_for_links(driver)
        
        # Step 2: Crawl energy billing links and json for content. 
        # In prod, we would want to use caching to avoid repeated calls.
        print("Opening links and parsing content...")

        for link_classification in parsed_links:
            # Gemini is returning a nested array for each billing type. 
            # In production we would want to provide a structured Gemini JSON response format, this is a little weird.
            for link in list(link_classification.values())[0]:
                # NOTE: I keep hitting Vertex API limits here so I'm just evaluating one billing URL.
                if (link["link_url"].endswith(BILLING_URL_SUFFIX_FOR_TESTING)):
                    # TODO: Replace hard-coded domain with relative link builder from webdriver current url.
                    driver.get("https://www.pse.com" + link["link_url"])
                    wait = WebDriverWait(driver, 20)
                    parsed_billing = crawl_for_billing(driver, "billing")
                    print(parsed_billing)

                    # Crawl json for billing data.
                    print("Crawling and evaluating json...")
                    filtered_json_responses = filter_driver_requests(driver)
                    parsed_json = crawl_json_for_billing(filtered_json_responses)
                    print(parsed_json)


    except Exception as e:
        print(f"\nAn error occurred: {e}")
        # In headless mode, saving a screenshot on error is crucial for debugging.
        screenshot_path = "error_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    finally:
        # 6. Always close the browser session to free up resources.
        print("Closing the browser.")
        driver.quit()

# NOTE: In prod, this would be called from a separate service processing each user instead of being run manually here.
if __name__ == "__main__":
    user = build_credentials()
    parse_data(user)