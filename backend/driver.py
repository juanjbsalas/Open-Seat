# driver.py
# Contains setupDriver() to initialize and return your browser driver

# Function to set up Selenium WebDriver
def setupDriver():
   options = Options()
   options.add_argument("--headless")  # Run in headless mode
   return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)