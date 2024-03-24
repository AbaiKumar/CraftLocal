from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

# Start a Selenium WebDriver session
driver = webdriver.Chrome()

# Open the web page where your Flask application is running
driver.get("http://127.0.0.1:5000")

# Simulate a request to the addItem route
# For demonstration purposes, we'll assume an itemID exists and the user is logged in
response = requests.get("http://127.0.0.1:5000/addItem?itemID=659d12224df34bb9a75e2a34")

# Check if the request was successful and the item was added
if response.status_code == 200:
    result = response.json()["result"]
    if result:
        print("Item added successfully!")
    else:
        print("Failed to add item.")
else:
    print("Failed to connect to the server.")

# Close the Selenium WebDriver session
driver.quit()
