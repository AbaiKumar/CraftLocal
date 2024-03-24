from selenium import webdriver
import time

# Assuming you already have the WebDriver initialized
driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000/signup")

# Define the test cases
signup_test_cases = [
    {
        "email": "invalid_email",
        "password": "password123",
        "confirm_password": "password123",
        "expected_result": "failure"
    },
    {
        "email": "test@example.com",
        "password": "password123",
        "confirm_password": "different_password",
        "expected_result": "failure"
    },
    {
        "email": "test@gmail.com",
        "password": "password123",
        "confirm_password": "password123",
        "expected_result": "success"
    },
]

# Function to execute signup test cases
def execute_signup_test_cases(driver):
    for test_case in signup_test_cases:
        try:
            # Find input fields
            email_field = driver.find_element("id", "mail")
            password_field = driver.find_element("id", "password")
            confirm_password_field = driver.find_element("id", "confirm_password")
            
            # Clear fields and input data
            email_field.clear()
            email_field.send_keys(test_case["email"])
            password_field.clear()
            password_field.send_keys(test_case["password"])
            confirm_password_field.clear()
            confirm_password_field.send_keys(test_case["confirm_password"])
            
            # Find and click the signup button
            signup_button = driver.find_element("id", "submit")
            signup_button.click()
            
            # Wait for page to load (you might need to adjust the timing here)
            time.sleep(2)

            print(test_case)
            
            # Check the expected result
            if test_case["expected_result"] == "success":
                # Assuming successful signup redirects to login page
                if "login" in driver.current_url:  
                    print("Signup Successful")
                else:
                    print("Invalid Username / password")

            elif test_case["expected_result"] == "failure":
                print("Test Failed: Invalid Username / password")

        except Exception as e:
            print(f"Exception occurred: {str(e)}")

# Execute the signup test cases
execute_signup_test_cases(driver)

# Close the browser
driver.quit()