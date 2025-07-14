# scheduler.py
# check_and_notify(driver, previous_courses)

    # Call scrapeCourses(driver)

    # Compare previous_courses vs new scrape

    # For new openings:

        # Call get_users_by_crn(crn)

        # Call send_sms() for each user

    # Return updated course dictionary

# Use schedule.every(5).minutes.do(...) to call this

from scraper import scrapeCourses 

# def notifier():


