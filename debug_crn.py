#!/usr/bin/env python3
"""
Debug script to check CRN issues
"""

from scraper import scrapeCourses
import json

def debug_scraper():
    """Debug the scraper to see what CRNs are actually being found"""
    print("🔍 Debugging CRN scraper...")
    print("=" * 50)
    
    try:
        # Run the scraper
        print("Fetching course data...")
        courses = scrapeCourses()
        
        print(f"✅ Found {len(courses)} total courses")
        print("\n📋 All available CRNs:")
        print("-" * 30)
        
        # Show all CRNs found
        crn_list = list(courses.keys())
        crn_list.sort()  # Sort for easier reading
        
        for i, crn in enumerate(crn_list[:20]):  # Show first 20
            course = courses[crn]
            print(f"{crn}: {course['subject']} {course['course_number']} - {course['title'][:40]}...")
            
        if len(crn_list) > 20:
            print(f"... and {len(crn_list) - 20} more courses")
            
        print(f"\n🔢 CRN Format Analysis:")
        print(f"Sample CRNs: {crn_list[:5]}")
        print(f"CRN lengths: {[len(crn) for crn in crn_list[:10]]}")
        print(f"Are they all digits? {[crn.isdigit() for crn in crn_list[:5]]}")
        
        # Save all CRNs to a file for reference
        with open("available_crns.txt", "w") as f:
            f.write("Available CRNs:\n")
            f.write("=" * 20 + "\n")
            for crn in crn_list:
                course = courses[crn]
                f.write(f"{crn}: {course['subject']} {course['course_number']} - {course['title']}\n")
        
        print(f"\n💾 Saved all CRNs to 'available_crns.txt'")
        
        # Test specific CRN lookup
        test_crn = input("\n🎯 Enter a CRN to test: ").strip()
        if test_crn in courses:
            course = courses[test_crn]
            print(f"✅ Found CRN {test_crn}:")
            print(f"   Subject: {course['subject']}")
            print(f"   Course: {course['course_number']}")
            print(f"   Title: {course['title']}")
            print(f"   Seats: {course['available_seats']}")
        else:
            print(f"❌ CRN {test_crn} not found")
            
            # Check for similar CRNs
            similar = [crn for crn in crn_list if test_crn in crn or crn in test_crn]
            if similar:
                print(f"🔍 Similar CRNs found: {similar[:5]}")
            else:
                print("🔍 No similar CRNs found")
                
        return courses
        
    except Exception as e:
        print(f"❌ Error running scraper: {str(e)}")
        print("\nPossible issues:")
        print("1. Website might be down")
        print("2. Website structure might have changed")
        print("3. Network connectivity issues")
        print("4. Chrome/ChromeDriver issues")
        return None

def test_website_access():
    """Test if we can access the website"""
    print("\n🌐 Testing website access...")
    
    try:
        from driver import setupDriver
        
        driver = setupDriver()
        driver.get("https://connect.wofford.edu/myWofford/registrar/courseSchedule.aspx")
        
        print(f"✅ Website title: {driver.title}")
        
        # Check if we can find the table
        from selenium.webdriver.common.by import By
        rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
        print(f"✅ Found {len(rows)} table rows")
        
        if len(rows) > 1:
            # Check first data row
            first_row = rows[1]
            columns = first_row.find_elements(By.TAG_NAME, "td")
            if columns:
                print(f"✅ First row has {len(columns)} columns")
                print(f"   Sample data: {[col.text.strip()[:20] for col in columns[:3]]}")
            else:
                print("❌ No columns found in first row")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Website access failed: {str(e)}")
        return False

def main():
    """Main debug function"""
    print("🧪 CRN Debug Tool")
    print("=" * 50)
    
    # Test 1: Website access
    website_ok = test_website_access()
    
    if not website_ok:
        print("\n⚠️ Can't access website. Check your internet connection.")
        return
    
    # Test 2: Scraper functionality  
    courses = debug_scraper()
    
    if courses:
        print(f"\n✅ Scraper working! Found {len(courses)} courses.")
        print("💡 Tips:")
        print("1. Check 'available_crns.txt' for all valid CRNs")
        print("2. Make sure you're using the exact CRN format")
        print("3. CRNs might be different than expected")
    else:
        print("\n❌ Scraper not working. Check your scraper.py file.")

if __name__ == "__main__":
    main()