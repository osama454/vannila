import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class MemoryGameTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the webdriver
        cls.driver = webdriver.Chrome()  # Make sure ChromeDriver is in your PATH
        cls.driver.get("http://localhost:3000/memory_game.html")  # Use the correct path to your local HTML file

    @classmethod
    def tearDownClass(cls):
        # Quit the browser after all tests
        cls.driver.quit()

    def test_grid_display(self):
        """ Test that a 4x3 grid of cards is displayed. """
        grid = self.driver.find_element(By.ID, 'game-grid')
        cards = grid.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(cards), 12, "The grid should contain 12 cards.")

    def test_card_flipping(self):
        """ Test that clicking a card flips it to reveal its value. """
        cards = self.driver.find_elements(By.CLASS_NAME, 'card')
        first_card = cards[0]
        first_card.click()

        # Check if the card is flipped
        self.assertIn('flipped', first_card.get_attribute('class'), "The card should be flipped when clicked.")
        self.assertTrue(first_card.text, "The card should reveal its value when flipped.")

    def test_card_matching(self):
        """ Test that selecting two cards reveals their values and matches them correctly. """
        cards = self.driver.find_elements(By.CLASS_NAME, 'card')
        first_card = cards[0]
        second_card = None

        # Find a card with the same value as the first card
        for card in cards[1:]:
            if card.get_attribute('data-value') == first_card.get_attribute('data-value'):
                second_card = card
                break

        first_card.click()
        second_card.click()

        # Wait for the match check to occur
        time.sleep(1)

        # Check if both cards are matched
        self.assertIn('matched', first_card.get_attribute('class'), "The first card should be matched.")
        self.assertIn('matched', second_card.get_attribute('class'), "The second card should be matched.")

    def test_victory_message(self):
        """ Test that the victory message appears when all pairs are matched. """
        cards = self.driver.find_elements(By.CLASS_NAME, 'card')

        # Create a dictionary to store card values and their corresponding elements
        card_pairs = {}
        
        # Loop through all cards and store them in the dictionary based on their value
        for card in cards:
            card_value = card.get_attribute('data-value')
            if card_value not in card_pairs:
                card_pairs[card_value] = [card]
            else:
                card_pairs[card_value].append(card)

        # Match all pairs by clicking the two cards with the same value
        for pair in card_pairs.values():
            first_card = pair[0]
            second_card = pair[1]
            
            first_card.click()
            time.sleep(0.15)
            second_card.click()

            # Wait a bit to allow the cards to be marked as matched
            time.sleep(1)

        # After all pairs are matched, wait for the alert to appear
        alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())

        # Check for the win alert
        self.assertEqual(alert.text, "You won!", "The win message should be displayed when all cards are matched.")
        alert.accept()  # Close the alert

    def test_random_shuffle(self):
        """ Test that the cards are shuffled when the game starts. """
        first_game_cards = [card.get_attribute('data-value') for card in self.driver.find_elements(By.CLASS_NAME, 'card')]

        # Refresh the page to start a new game
        self.driver.refresh()

        second_game_cards = [card.get_attribute('data-value') for card in self.driver.find_elements(By.CLASS_NAME, 'card')]

        # Ensure the order of cards is different
        self.assertNotEqual(first_game_cards, second_game_cards, "The cards should be shuffled every time the game starts.")

    def test_unmatched_cards_flip_back(self):
        """ Test that unmatched cards flip back after a delay. """
        cards = self.driver.find_elements(By.CLASS_NAME, 'card')

        # Select two non-matching cards
        first_card = cards[0]
        second_card = None
        for card in cards:
            if card.get_attribute('data-value') != first_card.get_attribute('data-value'):
                second_card = card
                break

        first_card.click()
        second_card.click()

        time.sleep(1.5)  # Wait for the delay

        # Check if both cards have flipped back
        self.assertNotIn('flipped', first_card.get_attribute('class'), "The first card should flip back if not matched.")
        self.assertNotIn('flipped', second_card.get_attribute('class'), "The second card should flip back if not matched.")

    def test_card_non_clickable_after_match(self):
        """ Test that matched cards are no longer clickable. """
        cards = self.driver.find_elements(By.CLASS_NAME, 'card')

        first_card = cards[0]
        second_card = None

        for card in cards[1:]:
            if card.get_attribute('data-value') == first_card.get_attribute('data-value'):
                second_card = card
                break

        first_card.click()
        second_card.click()
        time.sleep(1)  # Wait for the match

        # Try to click the matched cards again
        first_card.click()
        second_card.click()

        # Check if the cards are still matched and not flipped again
        self.assertIn('matched', first_card.get_attribute('class'), "The first card should not flip after matching.")
        self.assertIn('matched', second_card.get_attribute('class'), "The second card should not flip after matching.")

if __name__ == '__main__':
    unittest.main()
