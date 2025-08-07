import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setupDriver():
    """Set up Selenium WebDriver optimized for Railway"""
    options = Options()
    
    # Essential Railway options
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Memory and performance optimizations for Railway
    options.add_argument("--single-process")  # Use single process (important for Railway)
    options.add_argument("--no-zygote")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")
    options.add_argument("--disable-javascript")  # Disable JS if not needed
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--memory-pressure-off")
    
    # Network and loading optimizations
    options.add_argument("--aggressive-cache-discard")
    options.add_argument("--max_old_space_size=4096")
    
    # User agent to avoid detection
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Railway-specific
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        options.add_argument("--remote-debugging-port=9222")
        print("🚂 Running on Railway - using optimized settings")
    
    try:
        # Create the driver with increased timeouts
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Set aggressive timeouts for Railway
        driver.set_page_load_timeout(90)  # Increased timeout
        driver.implicitly_wait(20)        # Wait for elements
        
        print(f"✅ Chrome driver initialized successfully")
        return driver
        
    except Exception as e:
        print(f"❌ Error setting up Chrome driver: {str(e)}")
        raise e

def safe_get_page(driver, url, retries=3):
    """Safely load a page with retries"""
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}: Loading {url}")
            driver.get(url)
            
            # Wait for page to fully load
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Additional wait to ensure content is loaded
            time.sleep(5)
            
            print(f"✅ Page loaded successfully on attempt {attempt + 1}")
            return True
            
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retries - 1:
                time.sleep(10)  # Wait before retry
            else:
                raise e
    
    return False