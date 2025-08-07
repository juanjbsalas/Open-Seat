from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

from driver import setupDriver

# Constants
URL = "https://connect.wofford.edu/myWofford/registrar/courseSchedule.aspx"

# Function to scrape course data, returns dictionary w/ crn as key and course info as value.
def scrapeCourses():
    driver = setupDriver()
    driver.get(URL)
    
    # Add a small wait to ensure page loads
    time.sleep(3)
    
    # Find table rows (excluding headers)
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")[1:]
    
    print(f"DEBUG: Found {len(rows)} rows in table")  # Debug line

    # Dictionary to store course data
    courseDict = {}

    for i, row in enumerate(rows):
        columns = row.find_elements(By.TAG_NAME, "td")
        details = [col.text.strip() for col in columns]

        if details and len(details) >= 12:  # Ensures valid row structure
            crn = details[0].strip()  # CRN as the key, strip whitespace
            subject = details[1]
            course_number = details[2]
            title = details[10] if len(details) > 10 else "N/A"
            days = details[13] if len(details) > 13 else "N/A"
            time_slot = details[14] if len(details) > 14 else "N/A"
            instructor = details[20] if len(details) > 20 else "N/A"
            
            # Handle available seats more carefully
            try:
                available_seats = int(details[19]) if len(details) > 19 and details[19].isdigit() else 0
            except (ValueError, IndexError):
                available_seats = 0

            # Debug: Print first few CRNs
            if i < 5:
                print(f"DEBUG: Row {i}: CRN='{crn}', Subject='{subject}', Seats={available_seats}")

            courseDict[crn] = {
                "subject": subject,
                "course_number": course_number,
                "title": title,
                "days": days,
                "time": time_slot,
                "instructor": instructor,
                "available_seats": available_seats
            }
        else:
            # Debug: Show problematic rows
            if len(details) > 0:
                print(f"DEBUG: Skipped row {i} with {len(details)} columns: {details[:3]}...")

    print(f"DEBUG: Total courses found: {len(courseDict)}")  # Debug line
    print(f"DEBUG: Sample CRNs: {list(courseDict.keys())[:5]}")  # Debug line
    
    driver.quit()
    return courseDict