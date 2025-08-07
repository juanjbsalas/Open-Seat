# driver.py
# Contains setupDriver() to initialize and return your browser driver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to set up Selenium WebDriver
def setupDriver():
   options = Options()
   options.add_argument("--headless")  # Run in headless mode
   return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)