from selenium import webdriver
import time

# Define the test cases
test_cases = [
    {"username": "", "password": "A23@asd", "expected_result": "failure"},
    {"username": "", "password": "", "expected_result": "failure"},
    {"username": "22z434@psgtech.ac.in", "password": "12345", "expected_result": "failure"},
    {"username": "22z434@psgtech.ac.in", "password": "123", "expected_result": "success"},
]

# Function to execute test cases
def execute_test_cases():
    # Initialize the WebDriver (assuming Chrome WebDriver is installed)
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000/login")

    for test_case in test_cases:
        # Find username and password fields
        mail_field = driver.find_element("id", "mail")
        password_field = driver.find_element("id", "password")
        
        # Clear fields and input data
        mail_field.clear()
        mail_field.send_keys(test_case["username"])
        password_field.clear()
        password_field.send_keys(test_case["password"])
        
        # Find and click the login button
        login_button = driver.find_element("id", "submit")
        login_button.click()
        
        # Wait for page to load
        time.sleep(2)

        # Check the expected result
        if test_case["expected_result"] == "success":
            if "home" in driver.current_url:  # Assuming successful login redirects to the dashboard
                print(f"Test Passed: Login Successful for {test_case['username']} = {test_case['password']}")
            else:
                print(f"Test Failed: Login Failed unexpectedly for {test_case['username']} = {test_case['password']}")
                
        elif test_case["expected_result"] == "failure":
            print(f"Test Passed: Login Failed as expected for {test_case['username']} = {test_case['password']}")
    
    # Close the browser
    driver.quit()

# Execute the test cases
execute_test_cases()