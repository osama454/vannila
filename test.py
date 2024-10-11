import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class HabitTrackerTest(unittest.TestCase):
    def handle_alert(self):
        try:
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert_message = alert.text
            alert.accept()
            return alert_message
        except:
            return None

    def setUp(self):
        # Initialize the Chrome WebDriver (You can use other drivers if necessary)
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:3000/response")  # Assuming the app is running on localhost


    def test_practice_habit(self):
        driver = self.driver

        # Add a habit first
        habit_name_input = driver.find_element(By.ID, "habit-name")
        habit_count_input = driver.find_element(By.ID, "habit-count")
        submit_button = driver.find_element(By.ID, "submit-habit")
        
        habit_name_input.send_keys("Exercise")
        habit_count_input.send_keys("5")
        submit_button.click()
        
        # Requirement 3: Practice button must increment the counter
        practice_button = driver.find_element(By.ID, "practice-exercise")
        practice_button.click()
        
        counter_display = driver.find_element(By.ID, "counter-exercise")
        self.assertIn("1/5", counter_display.text)
        
        # Requirement 5: Practice button must disable after completing all
        for _ in range(4):
            practice_button = driver.find_element(By.ID, "practice-exercise")
            practice_button.click()
        alert = self.handle_alert()
        self.handle_alert()
        practice_button = driver.find_element(By.ID, "practice-exercise")
        self.assertEqual(practice_button.get_property('disabled'), True)
        
        # Requirement 6: Alert after completing the habit
        self.assertEqual(alert, "You completed your Exercise habit!")
    def test_add_habit(self):
        driver = self.driver
        
        # Requirement 1: Test adding a habit with a name and count
        habit_name_input = driver.find_element(By.ID, "habit-name")
        habit_count_input = driver.find_element(By.ID, "habit-count")
        submit_button = driver.find_element(By.ID, "submit-habit")
        
        habit_name_input.send_keys("Exercise")
        habit_count_input.send_keys("5")
        submit_button.click()
        
        # Requirement 2: Habit should be added to the list
        habit_list = driver.find_element(By.ID, "habits-container")
        self.assertIn("Exercise", habit_list.text)
        self.assertIn("0/5", habit_list.text)
        

   
    def test_complete_all_habits(self):
          driver = self.driver
  
          # Add multiple habits
          habit_name_input = driver.find_element(By.ID, "habit-name")
          habit_count_input = driver.find_element(By.ID, "habit-count")
          submit_button = driver.find_element(By.ID, "submit-habit")
          
          habits = [("Exercise", 3), ("Reading", 2)]
          
          for name, count in habits:
              habit_name_input.send_keys(name)
              habit_count_input.send_keys(count)
              submit_button.click()
          
          # Practice both habits
          practice_button_exercise = driver.find_element(By.ID, "practice-exercise")
          
          
          for _ in range(3):
              
              practice_button_exercise = driver.find_element(By.ID, "practice-exercise")
              practice_button_exercise.click()
          
          self.handle_alert()
          
          for _ in range(2):
              practice_button_reading = driver.find_element(By.ID, "practice-reading")
              practice_button_reading.click()
          self.handle_alert()
          # Requirement 7: Alert after completing all habits
          alert = self.handle_alert()
          self.assertEqual(alert, "You have completed all your habits!")
  
  
    def test_invalid_habit_input(self):
          driver = self.driver
  
          # Requirement 8: Invalid input should show an alert
          habit_name_input = driver.find_element(By.ID, "habit-name")
          habit_count_input = driver.find_element(By.ID, "habit-count")
          submit_button = driver.find_element(By.ID, "submit-habit")
          
          habit_name_input.send_keys("Exercise")
          habit_count_input.send_keys("0")  # Invalid count
          
          submit_button.click()
          
          alert = driver.switch_to.alert
          self.assertEqual(alert.text, "Please enter a valid habit name and count.")
          alert.accept()
  
    def test_reset_form_after_adding_habit(self):
          driver = self.driver
          
          # Requirement 9: Input fields should reset after adding a habit
          habit_name_input = driver.find_element(By.ID, "habit-name")
          habit_count_input = driver.find_element(By.ID, "habit-count")
          submit_button = driver.find_element(By.ID, "submit-habit")
          
          habit_name_input.send_keys("Exercise")
          habit_count_input.send_keys("5")
          submit_button.click()
          
          self.assertEqual(habit_name_input.get_attribute('value'), '')
          self.assertEqual(habit_count_input.get_attribute('value'), '')
  
    def test_render_habits_after_updates(self):
          driver = self.driver
          
          # Requirement 10: Habit list should re-render after updates
          habit_name_input = driver.find_element(By.ID, "habit-name")
          habit_count_input = driver.find_element(By.ID, "habit-count")
          submit_button = driver.find_element(By.ID, "submit-habit")
          
          habit_name_input.send_keys("Exercise")
          habit_count_input.send_keys("5")
          submit_button.click()
  
          habit_list = driver.find_element(By.ID, "habits-container")
          self.assertIn("Exercise", habit_list.text)
          
          practice_button = driver.find_element(By.ID, "practice-exercise")
          practice_button.click()
          
          habit_list = driver.find_element(By.ID, "habits-container")
          self.assertIn("1/5", habit_list.text)
  
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
