import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class TestMoodBoardApp(unittest.TestCase):

    def setUp(self):
        # Setup Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:3000/mood_board.html")  # Assuming the app is hosted locally

    def tearDown(self):
        # Quit WebDriver after each test
        self.driver.quit()

    def test_add_and_delete_card(self):
        driver = self.driver

        # Add a new card and check if it's added to the board
        add_card_button = driver.find_element(By.ID, "add-card-btn")
        add_card_button.click()
        mood_card = driver.find_element(By.CLASS_NAME, "mood-card")
        self.assertIsNotNone(mood_card, "Mood card should be created.")

        # Select the newly created card
        mood_card.click()
        self.assertIn("selected", mood_card.get_attribute("class"), "Card should be selectable.")

        # Delete the selected card and check if it's removed
        delete_card_button = driver.find_element(By.ID, "delete-card-btn")
        delete_card_button.click()
        self.assertEqual(len(driver.find_elements(By.CLASS_NAME, "mood-card")), 0, "Mood card should be deleted.")

    def test_color_change(self):
        driver = self.driver

        # Add a card and select it
        add_card_button = driver.find_element(By.ID, "add-card-btn")
        add_card_button.click()
        mood_card = driver.find_element(By.CLASS_NAME, "mood-card")
        mood_card.click()

        # Change the background color of the selected card
        color_button = driver.find_element(By.ID, "color-red")  # Assuming a red button exists with ID color-red
        color_button.click()
        self.assertEqual(mood_card.value_of_css_property("background-color"), "rgba(255, 0, 0, 1)", "Card background color should be red.")

    def test_add_text_to_card(self):
        driver = self.driver

        # Add a card and select it
        add_card_button = driver.find_element(By.ID, "add-card-btn")
        add_card_button.click()
        mood_card = driver.find_element(By.CLASS_NAME, "mood-card")
        mood_card.click()

        # Add text to the card
        text_dropdown = driver.find_element(By.ID, "text-options")  # Assuming text dropdown has an ID
        text_dropdown.click()
        option = driver.find_element(By.XPATH, "//option[@value='quote1']")
        option.click()

        # Verify that the selected text appears in the card
        card_text = mood_card.find_element(By.CLASS_NAME, "card-text").text
        self.assertEqual(card_text, "quote1", "The selected text should be displayed in the card.")

    def test_slider_movement(self):
        driver = self.driver

        # Add a card and select it
        add_card_button = driver.find_element(By.ID, "add-card-btn")
        add_card_button.click()
        mood_card = driver.find_element(By.CLASS_NAME, "mood-card")
        mood_card.click()

        # Move the text position using sliders
        x_slider = driver.find_element(By.ID, "x-slider")  # Assuming the slider has an ID of x-slider
        y_slider = driver.find_element(By.ID, "y-slider")  # Assuming the slider has an ID of y-slider

        action = ActionChains(driver)
        action.click_and_hold(x_slider).move_by_offset(30, 0).release().perform()
        action.click_and_hold(y_slider).move_by_offset(0, 30).release().perform()

        # Check the CSS position of the text element inside the card
        card_text = mood_card.find_element(By.CLASS_NAME, "card-text")
        x_position = card_text.value_of_css_property("left")
        y_position = card_text.value_of_css_property("top")
        self.assertNotEqual(x_position, "0px", "Text X position should change.")
        self.assertNotEqual(y_position, "0px", "Text Y position should change.")

    def test_controls_disabled_when_no_card_selected(self):
        driver = self.driver

        # Check if controls are disabled without card selection
        color_button = driver.find_element(By.ID, "color-red")  # Assuming a color button exists
        text_dropdown = driver.find_element(By.ID, "text-options")
        x_slider = driver.find_element(By.ID, "x-slider")
        y_slider = driver.find_element(By.ID, "y-slider")

        self.assertFalse(color_button.is_enabled(), "Color button should be disabled when no card is selected.")
        self.assertFalse(text_dropdown.is_enabled(), "Text dropdown should be disabled when no card is selected.")
        self.assertFalse(x_slider.is_enabled(), "X slider should be disabled when no card is selected.")
        self.assertFalse(y_slider.is_enabled(), "Y slider should be disabled when no card is selected.")

    def test_single_card_selection(self):
        driver = self.driver

        # Add two cards
        add_card_button = driver.find_element(By.ID, "add-card-btn")
        add_card_button.click()
        add_card_button.click()

        cards = driver.find_elements(By.CLASS_NAME, "mood-card")
        card1, card2 = cards[0], cards[1]

        # Select the first card and ensure it's the only one selected
        card1.click()
        self.assertIn("selected", card1.get_attribute("class"), "First card should be selected.")
        self.assertNotIn("selected", card2.get_attribute("class"), "Second card should not be selected.")

        # Now select the second card and ensure only it is selected
        card2.click()
        self.assertIn("selected", card2.get_attribute("class"), "Second card should be selected.")
        self.assertNotIn("selected", card1.get_attribute("class"), "First card should not be selected.")

if __name__ == "__main__":
    unittest.main()
