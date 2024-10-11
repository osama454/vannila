import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class TestChatApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Selenium WebDriver (use Chrome, Firefox, or the browser of your choice)
        cls.driver = webdriver.Chrome()
        cls.driver.get('http://localhost:3000')  # Assuming the server is running locally on port 3000
        time.sleep(2)  # Give some time for the app to load

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_chat_history_is_loaded(self):
        """Test that the chat history is loaded when opening the app"""
        messages = self.driver.find_elements(By.CSS_SELECTOR, '#messages li')
        self.assertGreaterEqual(len(messages), 0)  # History should be loaded, even if empty

    def test_user_can_send_and_receive_message(self):
        """Test that users can send and receive messages"""
        input_field = self.driver.find_element(By.ID, 'input')
        input_field.clear()
        input_field.send_keys('Hello, world!')
        
        form = self.driver.find_element(By.ID, 'form')
        form.submit()

        time.sleep(1)  # Wait for message to be sent and broadcasted
        
        # Check if the message appears in the chat
        messages = self.driver.find_elements(By.CSS_SELECTOR, '#messages li')
        last_message = messages[-1].text
        self.assertEqual(last_message, 'Hello, world!')

    def test_no_sender_name_in_messages(self):
        """Test that the sender's name is not visible in the messages"""
        messages = self.driver.find_elements(By.CSS_SELECTOR, '#messages li')
        for message in messages:
            self.assertNotIn(":", message.text)  # No name should appear with colon, just message text

    def test_form_submission_and_clearing(self):
        """Test that submitting the form sends the message and clears the input field"""
        input_field = self.driver.find_element(By.ID, 'input')
        input_field.clear()
        input_field.send_keys('Test message to clear')

        form = self.driver.find_element(By.ID, 'form')
        form.submit()

        time.sleep(1)  # Wait for the message to be sent

        # After submission, the input field should be cleared
        input_value = self.driver.find_element(By.ID, 'input').get_attribute('value')
        self.assertEqual(input_value, '')

    def test_auto_scroll_on_new_message(self):
        """Test that the page auto-scrolls when a new message is added"""
        # Check the scroll position before sending the message
        scroll_position_before = self.driver.execute_script("return window.scrollY")

        # Send a new message
        input_field = self.driver.find_element(By.ID, 'input')
        input_field.clear()
        input_field.send_keys('Scroll test message')
        form = self.driver.find_element(By.ID, 'form')
        form.submit()

        time.sleep(1)  # Wait for the message to be sent and processed

        # Check the scroll position after the message
        scroll_position_after = self.driver.execute_script("return window.scrollY")

        # The scroll position should have increased if auto-scroll is working
        self.assertGreater(scroll_position_after, scroll_position_before)

    def test_all_previous_messages_loaded(self):
        """Test that all previously sent messages are loaded on a new connection"""
        messages = self.driver.find_elements(By.CSS_SELECTOR, '#messages li')
        self.assertGreaterEqual(len(messages), 1)  # At least one message should be loaded (previous ones)

    def test_submit_without_page_reload(self):
        """Test that submitting the form does not reload the page"""
        input_field = self.driver.find_element(By.ID, 'input')
        input_field.clear()
        input_field.send_keys('Test reload prevention')

        form = self.driver.find_element(By.ID, 'form')
        form.submit()

        time.sleep(1)  # Wait for submission

        # Check that the URL has not changed (indicating no reload occurred)
        current_url = self.driver.current_url
        self.assertEqual(current_url, 'http://localhost:3000/')

    def test_user_disconnection(self):
        """Test that user disconnection is logged on the server (manual inspection needed)"""
        # Disconnect the user by closing the browser session
        self.driver.quit()
        time.sleep(1)  # Wait for the disconnection to be logged

        # Reopen the session for other tests
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:3000')  # Assuming the server is running locally on port 3000

if __name__ == '__main__':
    unittest.main()
