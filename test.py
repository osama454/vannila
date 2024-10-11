import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TestFileManager(unittest.TestCase):

    def setUp(self):
        # Set up Selenium WebDriver (using ChromeDriver as an example)
        self.driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH
        self.driver.get("http://localhost:3000/ideal")  # Path to your HTML file

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

    def test_path_display(self):
        # Test Requirement 1: Current path is displayed correctly
        driver = self.driver
        path_elements = driver.find_elements(By.CSS_SELECTOR, "#path span")
        self.assertGreater(len(path_elements), 0)
        self.assertEqual(path_elements[0].text, "root")

    def test_folder_navigation(self):
        # Test Requirement 3: Navigating into a folder updates the path
        driver = self.driver
        # Create a folder to test navigation
        create_folder_btn = driver.find_element(By.ID, "create-folder-btn")
        create_folder_btn.click()
        alert = driver.switch_to.alert
        alert.send_keys("TestFolder")
        alert.accept()
        
        # Click on the newly created folder
        folder_item = driver.find_element(By.XPATH, "//div[@class='item folder-item' and text()='TestFolder']")
        folder_item.click()

        # Check that the path is updated
        path_elements = driver.find_elements(By.CSS_SELECTOR, "#path span")
        self.assertEqual(path_elements[-1].text, "TestFolder")

    def test_file_display_and_edit(self):
        # Test Requirement 4: File content is displayed and editable
        driver = self.driver
        # Create a file
        create_file_btn = driver.find_element(By.ID, "create-file-btn")
        create_file_btn.click()
        alert = driver.switch_to.alert
        alert.send_keys("TestFile")
        alert.accept()

        # Click on the file to open it
        file_item = driver.find_element(By.XPATH, "//div[@class='item file-item' and text()='TestFile']")
        file_item.click()

        # Check if file content area is displayed and editable
        file_content_div = driver.find_element(By.ID, "file-content")
        self.assertTrue(file_content_div.is_displayed())
        file_text_area = driver.find_element(By.ID, "file-text")
        file_text_area.send_keys("Test content for the file.")
        save_btn = driver.find_element(By.ID, "save-btn")
        save_btn.click()
        alert = driver.switch_to.alert
        self.assertEqual(alert.text, "File saved!")
        alert.accept()

    def test_create_file(self):
        # Test Requirement 6: Create a new file in the current directory
        driver = self.driver
        create_file_btn = driver.find_element(By.ID, "create-file-btn")
        create_file_btn.click()
        alert = driver.switch_to.alert
        alert.send_keys("NewFile")
        alert.accept()

        # Check if the new file appears in the file container
        file_item = driver.find_element(By.XPATH, "//div[@class='item file-item' and text()='NewFile']")
        self.assertIsNotNone(file_item)

    def test_create_folder(self):
        # Test Requirement 6: Create a new folder in the current directory
        driver = self.driver
        create_folder_btn = driver.find_element(By.ID, "create-folder-btn")
        create_folder_btn.click()
        alert = driver.switch_to.alert
        alert.send_keys("NewFolder")
        alert.accept()

        # Check if the new folder appears in the folder container
        folder_item = driver.find_element(By.XPATH, "//div[@class='item folder-item' and text()='NewFolder']")
        self.assertIsNotNone(folder_item)

    def test_save_file(self):
        # Test Requirement 5: Save file content
        driver = self.driver
        # Create a file
        create_file_btn = driver.find_element(By.ID, "create-file-btn")
        create_file_btn.click()
        alert = driver.switch_to.alert
        alert.send_keys("FileToSave")
        alert.accept()

        # Open the file and edit it
        file_item = driver.find_element(By.XPATH, "//div[@class='item file-item' and text()='FileToSave']")
        file_item.click()
        file_text_area = driver.find_element(By.ID, "file-text")
        file_text_area.send_keys("This is the new content.")
        save_btn = driver.find_element(By.ID, "save-btn")
        save_btn.click()

        # Verify save confirmation alert
        alert = driver.switch_to.alert
        self.assertEqual(alert.text, "File saved!")
        alert.accept()

    def test_path_navigation(self):
        # Test Requirement 7: Navigate back by clicking on the path
        driver = self.driver
        # Create and navigate to a folder
        create_folder_btn = driver.find_element(By.ID, "create-folder-btn")
        create_folder_btn.click()
        alert = driver.switch_to.alert
        alert.send_keys("Folder1")
        alert.accept()

        folder_item = driver.find_element(By.XPATH, "//div[@class='item folder-item' and text()='Folder1']")
        folder_item.click()

        # Navigate back by clicking on "root" in the path
        root_path = driver.find_element(By.XPATH, "//span[text()='root']")
        root_path.click()

        # Check that we are back in the root folder
        path_elements = driver.find_elements(By.CSS_SELECTOR, "#path span")
        self.assertEqual(path_elements[-1].text, "root")

if __name__ == "__main__":
    unittest.main()
