import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class TestAuthApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the WebDriver (Chrome in this case)
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:3000")  # Make sure your server is running

    @classmethod
    def tearDownClass(cls):
        # Tear down the WebDriver
        cls.driver.quit()

    def test_01_homepage(self):
        """Test if the homepage loads and has the correct links."""
        driver = self.driver
        self.assertIn("Welcome to the Authentication App", driver.page_source)
        self.assertIn("Sign Up", driver.page_source)
        self.assertIn("Sign In", driver.page_source)
        time.sleep(1)
        
    def test_02_signup(self):
        """Test the signup functionality."""
        driver = self.driver
        driver.get("http://localhost:3000/signup")
        
        # Fill in the sign-up form
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        # Submit the form
        password_input.send_keys(Keys.RETURN)

        # Check for redirection to the sign-in page
        time.sleep(1)  # Give the server time to process
        self.assertIn("Sign In", driver.page_source)
    
    def test_03_signup_existing_user(self):
        """Test the signup functionality with an existing username."""
        driver = self.driver
        driver.get("http://localhost:3000/signup")
        
        # Fill in the sign-up form with a username that already exists
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("testuser")  # Assuming "testuser" already exists
        password_input.send_keys("password123")
        
        # Submit the form
        password_input.send_keys(Keys.RETURN)

        # Check if the "Username already exists" message appears
        time.sleep(1)  # Give the server time to process
        self.assertIn("Username already exists", driver.page_source)

    def test_04_signin_valid(self):
        """Test signing in with valid credentials."""
        driver = self.driver
        driver.get("http://localhost:3000/signin")

        # Fill in the sign-in form
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        # Submit the form
        password_input.send_keys(Keys.RETURN)

        # Check if the hello message appears
        time.sleep(1)  # Give the server time to process
        self.assertIn("Hello, testuser", driver.page_source)

    def test_05_signin_invalid(self):
        """Test signing in with invalid credentials."""
        driver = self.driver
        driver.get("http://localhost:3000/signin")

        # Fill in the sign-in form with wrong credentials
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("wronguser")
        password_input.send_keys("wrongpassword")
        
        # Submit the form
        password_input.send_keys(Keys.RETURN)

        # Check if the error message appears
        time.sleep(1)  # Give the server time to process
        self.assertIn("Invalid username or password", driver.page_source)

if __name__ == '__main__':
    unittest.main()
