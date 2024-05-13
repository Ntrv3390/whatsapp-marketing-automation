from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import csv

# Config
login_time = 60                 # Time for login (in seconds)
new_msg_time = 24                # TTime for a new message (in seconds)
send_msg_time = 15               # Time for sending a message (in seconds)
country_code = 91                # Set your country code
action_time = 15                 # Set time for button click action
abs_path = r'absolute path to your project'
image_path = fr'{abs_path}\image name with extention' # Absolute path to you image
chrome_profile_path = 'Chrome profile path'  # Your Chrome profile path 

# Create Chrome options
chrome_options = Options()
chrome_options.add_argument(f'--user-data-dir={chrome_profile_path}')

# Create driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
print("Starting sending the messages...")

# Encode Message Text
with open('message txt file path here', 'r', encoding='utf-8') as file:
    msg = file.read()

# Open browser with default link
link = 'https://web.whatsapp.com'
driver.get(link)
time.sleep(login_time)

# Loop Through Numbers List
file_number = 42
while True:
    filename = f'numbers csv file here'
    print(f"Currently working on {filename}")
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header if exists
            for row in reader:
                num = row[0]  # Assuming the phone numbers start from column 1 (index 1)
                link = f'https://web.whatsapp.com/send/?phone={country_code}{num}'
                try:
                    driver.get(link)
                except WebDriverException as e:
                    print(f"An error occurred while trying to get the link. Phone number: {num}. ", e)
                    continue
                time.sleep(new_msg_time)
                # Click on button to load the input DOM
                attach_btn = driver.find_element(By.CSS_SELECTOR, '._ak1o')
                attach_btn.click()
                time.sleep(action_time)
                # Find and send image path to input
                elements = driver.find_elements(By.CSS_SELECTOR, '.x1c4vz4f input')
                if len(elements) >= 2:
                    msg_input = elements[1]
                else:
                    print("Error occurred in finding Pics element")
                    break
                msg_input.send_keys(image_path)
                time.sleep(action_time)
                # Start the action chain to write the message
                actions = ActionChains(driver)
                for line in msg.split('\n'):
                    actions.send_keys(line)
                    # SHIFT + ENTER to create next line
                    actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
                actions.send_keys(Keys.ENTER)
                actions.perform()
                time.sleep(send_msg_time)
        file_number += 1
        time.sleep(900)
    except FileNotFoundError:
        print(f"No more files found. Finished processing.")
        break


print("All the messages sent successfully.")
# Quit the driver
driver.quit()