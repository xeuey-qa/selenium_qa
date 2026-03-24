from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class DakMainPage:
    def __init__(self,browser):
        self.browser = browser
        self.url = "https://duckduckgo.com"
        self.SEARCH_FIELD = (By.NAME, "q")
        
    
    def open(self):
        self.browser.get(self.url)

    def search_for(self,text):
        field = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(self.SEARCH_FIELD)
        )
        field.send_keys(text + Keys.ENTER)

        