from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Define your LinkedIn credentials
username = ''
password = ''

# Path to your ChromeDriver
DRIVER_PATH = './chromedriver-win32/chromedriver.exe'  # Make sure this path is correct

# Initialize WebDriver
service = Service(DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=service, options=options)

# Function to log into LinkedIn
def linkedin_login():
    driver.get('https://www.linkedin.com/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'feed-identity-module')]")))

# Function to send a connection request
def send_connection_request(profile_url):
    driver.get(profile_url)
    time.sleep(3)  # Wait for the page to load
    try:
        connect_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action')]"))
        )
        # Scroll the button into view using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", connect_button)
        time.sleep(1)  # Wait for the element to be in view
        
        # Try clicking using JavaScript to avoid interception
        driver.execute_script("arguments[0].click();", connect_button)
        add_note_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Add a note']")))
        add_note_button.click()
        note_textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//textarea[@name='message']")))
        note_textarea.send_keys('Hi, I would like to connect with you on LinkedIn.')
        send_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Send invitation']")))
        send_button.click()
        print(f"Connection request sent to {profile_url}")
    except Exception as e:
        print(f"Failed to send connection request to {profile_url}: {e}")

# Log into LinkedIn
linkedin_login()

# List of LinkedIn profile URLs to send connection requests to
profiles = [
    'https://www.linkedin.com/in/imtiaz-hussain-40a552263/',
    'https://www.linkedin.com/in/muhammad-faizan-jamshaid-a21591241/',
    'https://www.linkedin.com/in/adiba-abid-2658b9199/',
    'https://www.linkedin.com/in/ghulamrasool1/',
    # Add more profiles as needed
]

# Send connection requests
for profile in profiles:
    send_connection_request(profile)
    time.sleep(5)  # Add delay to avoid being flagged as a bot

# Close the driver
driver.quit()
