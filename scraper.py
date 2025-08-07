import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver import setupDriver, safe_get_page

# Constants
URL = "https://connect.wofford.edu/myWofford/registrar/courseSchedule.aspx"

def scrapeCourses():
    """Scrape course data with robust error handling for Railway"""
    driver = None
    
    try:
        print(f"🔍 Starting course scraping...")
        print(f"Environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'Local')}")
        
        # Initialize driver
        driver = setupDriver()
        print(f"✅ Driver initialized")
        
        # Load the page with retries
        print(f"📡 Loading course catalog: {URL}")
        if not safe_get_page(driver, URL):
            raise Exception("Failed to load course catalog after retries")
        
        print(f"✅ Course catalog loaded")
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Find all tables
        print(f"🔍 Looking for course tables...")
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"Found {len(tables)} table(s)")
        
        if not tables:
            # Try alternative selectors
            print("❌ No tables found with TAG_NAME. Trying CSS selectors...")
            tables = driver.find_elements(By.CSS_SELECTOR, "table")
            print(f"CSS selector found {len(tables)} table(s)")
            
        if not tables:
            # Save page source for debugging
            page_source = driver.page_source
            print(f"❌ No tables found. Page source length: {len(page_source)}")
            print(f"Page source preview: {page_source[:1000]}...")
            raise Exception("No course tables found on the page")
        
        # Get the main table (usually the first or largest one)
        main_table = tables[0]
        if len(tables) > 1:
            # Find the table with the most rows
            main_table = max(tables, key=lambda t: len(t.find_elements(By.TAG_NAME, "tr")))
        
        # Find table rows (excluding headers)
        all_rows = main_table.find_elements(By.TAG_NAME, "tr")
        data_rows = all_rows[1:] if len(all_rows) > 1 else all_rows
        
        print(f"📊 Found {len(all_rows)} total rows, {len(data_rows)} data rows")
        
        if len(data_rows) == 0:
            raise Exception("No data rows found in course table")
        
        # Dictionary to store course data
        courseDict = {}
        
        for i, row in enumerate(data_rows):
            try:
                columns = row.find_elements(By.TAG_NAME, "td")
                details = [col.text.strip() for col in columns]
                
                # Debug first few rows
                if i < 3:
                    print(f"Row {i}: {len(columns)} columns, first 5 values: {details[:5]}")
                
                if details and len(details) >= 12:  # Minimum required columns
                    crn = details[0].strip()
                    
                    # Skip empty CRNs
                    if not crn or not crn.replace('-', '').replace(' ', ''):
                        continue
                    
                    # Extract course information with safe indexing
                    subject = details[1] if len(details) > 1 else "N/A"
                    course_number = details[2] if len(details) > 2 else "N/A"
                    title = details[10] if len(details) > 10 else "N/A"
                    days = details[13] if len(details) > 13 else "N/A"
                    time_slot = details[14] if len(details) > 14 else "N/A"
                    instructor = details[20] if len(details) > 20 else "N/A"
                    
                    # Handle available seats more carefully
                    available_seats = 0
                    if len(details) > 19:
                        try:
                            seats_text = details[19].strip()
                            if seats_text.isdigit():
                                available_seats = int(seats_text)
                        except (ValueError, IndexError):
                            available_seats = 0
                    
                    courseDict[crn] = {
                        "subject": subject,
                        "course_number": course_number,
                        "title": title,
                        "days": days,
                        "time": time_slot,
                        "instructor": instructor,
                        "available_seats": available_seats
                    }
                    
                    # Debug first few courses
                    if i < 3:
                        print(f"✅ Parsed course: CRN {crn}, {subject} {course_number}, {available_seats} seats")
                
            except Exception as row_error:
                print(f"⚠️ Error parsing row {i}: {str(row_error)}")
                continue
        
        print(f"🎉 Successfully scraped {len(courseDict)} courses")
        
        # Show sample of scraped data
        if courseDict:
            sample_crns = list(courseDict.keys())[:3]
            print(f"📋 Sample courses:")
            for crn in sample_crns:
                course = courseDict[crn]
                print(f"   {crn}: {course['subject']} {course['course_number']} - {course['available_seats']} seats")
        
        return courseDict
        
    except Exception as e:
        error_msg = f"❌ Scraping failed: {str(e)}"
        print(error_msg)
        print(f"Full traceback: {traceback.format_exc()}")
        
        # Try to save screenshot for debugging
        if driver:
            try:
                driver.save_screenshot("/tmp/scraper_error.png")
                print("📸 Error screenshot saved")
            except:
                pass
        
        # Return empty dict instead of raising exception
        return {}
        
    finally:
        # Always clean up
        if driver:
            try:
                driver.quit()
                print("✅ Driver closed")
            except:
                pass