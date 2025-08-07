import os
import logging
from flask import Flask, request, render_template, jsonify, redirect, url_for
import threading
import time
import json
from datetime import datetime
from scraper import scrapeCourses
from notifier import send_email

app = Flask(__name__)

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Production configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    PORT = int(os.environ.get('PORT', 5000))

app.config.from_object(Config)

# In-memory storage for user requests (you can replace this with a database later)
user_requests = []
active_monitors = {}  # Track active monitoring threads

# File to persist user requests
DATA_FILE = "user_requests.json"

def load_user_requests():
    """Load user requests from JSON file"""
    global user_requests
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                user_requests = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            user_requests = []
    else:
        user_requests = []

def save_user_requests():
    """Save user requests to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(user_requests, f, indent=2)

def check_course_availability(crn, user_data):
    """Background function to check course availability for a specific user"""
    print(f"Starting monitoring for CRN {crn} for user {user_data['email']}")
    
    while crn in active_monitors:
        try:
            # Scrape current course data
            courses = scrapeCourses()
            
            if crn in courses and courses[crn]['available_seats'] > 0:
                # Course is available! Send notification
                course_info = courses[crn]
                subject = f"🎉 Seat Available in {course_info['subject']} {course_info['course_number']}"
                
                body = f"""Hi {user_data['name']},

Great news! A seat has become available in your requested course:

Course: {course_info['subject']} {course_info['course_number']} - {course_info['title']}
CRN: {crn}
Available Seats: {course_info['available_seats']}
Instructor: {course_info['instructor']}
Schedule: {course_info['days']} at {course_info['time']}

Please log into your student portal immediately to register for this course.

Best of luck!
Open Seat Notification System
"""
                
                send_email(user_data['email'], subject, body)
                print(f"Notification sent to {user_data['email']} for CRN {crn}")
                
                # Remove from active monitoring and user requests
                if crn in active_monitors:
                    del active_monitors[crn]
                
                # Remove the user request from the list
                global user_requests
                user_requests = [req for req in user_requests if not (req['crn'] == crn and req['email'] == user_data['email'])]
                save_user_requests()
                
                break
            else:
                # Course not available, continue monitoring
                available_seats = courses.get(crn, {}).get('available_seats', 0)
                print(f"CRN {crn} still has {available_seats} seats. Continuing to monitor...")
                
        except Exception as e:
            print(f"Error checking course availability for CRN {crn}: {str(e)}")
        
        # Wait before checking again (5 minutes)
        time.sleep(300)  # 300 seconds = 5 minutes
    
    print(f"Stopped monitoring CRN {crn}")

@app.route('/')
def index():
    """Main page with the form"""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_request():
    """Handle form submission"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        crn = request.form.get('crn', '').strip()
        
        # Basic validation
        if not all([name, email, crn]):
            return render_template('index.html', error="Please fill in all required fields.")
        
        # Check if CRN exists in the course catalog
        try:
            courses = scrapeCourses()
            if crn not in courses:
                return render_template('index.html', error=f"CRN {crn} not found in the course catalog.")
        except Exception as e:
            return render_template('index.html', error="Error accessing course catalog. Please try again later.")
        
        # Check if already monitoring this CRN for this user
        existing_request = next((req for req in user_requests if req['crn'] == crn and req['email'] == email), None)
        if existing_request:
            return render_template('index.html', error="You are already monitoring this course.")
        
        # Create user request
        user_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'crn': crn,
            'timestamp': datetime.now().isoformat(),
            'course_info': courses[crn]
        }
        
        # Add to user requests
        user_requests.append(user_data)
        save_user_requests()
        
        # Start monitoring thread if not already active for this CRN
        if crn not in active_monitors:
            monitor_thread = threading.Thread(target=check_course_availability, args=(crn, user_data), daemon=True)
            active_monitors[crn] = monitor_thread
            monitor_thread.start()
        
        return render_template('success.html', 
                             name=name, 
                             crn=crn, 
                             course_info=courses[crn])
        
    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {str(e)}")

@app.route('/status')
def status():
    """Show current monitoring status"""
    return render_template('status.html', 
                         user_requests=user_requests, 
                         active_monitors=list(active_monitors.keys()))

@app.route('/api/courses/<crn>')
def get_course_info(crn):
    """API endpoint to get course information"""
    try:
        courses = scrapeCourses()
        if crn in courses:
            return jsonify(courses[crn])
        else:
            return jsonify({'error': 'CRN not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/remove/<crn>/<email>')
def remove_request(crn, email):
    """Remove a monitoring request"""
    global user_requests
    user_requests = [req for req in user_requests if not (req['crn'] == crn and req['email'] == email)]
    save_user_requests()
    
    # If no more requests for this CRN, stop monitoring
    crn_requests = [req for req in user_requests if req['crn'] == crn]
    if not crn_requests and crn in active_monitors:
        del active_monitors[crn]
    
    return redirect(url_for('status'))

def start_existing_monitors():
    """Restart monitoring for existing requests when the app starts"""
    load_user_requests()
    crn_groups = {}
    
    # Group requests by CRN
    for request in user_requests:
        crn = request['crn']
        if crn not in crn_groups:
            crn_groups[crn] = []
        crn_groups[crn].append(request)
    
    # Start monitoring threads for each unique CRN
    for crn, requests in crn_groups.items():
        if crn not in active_monitors:
            # Use the first request's data for monitoring (all users with same CRN will be notified)
            monitor_thread = threading.Thread(target=check_course_availability, args=(crn, requests[0]), daemon=True)
            active_monitors[crn] = monitor_thread
            monitor_thread.start()

# Add a health check endpoint for Railway
@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'active_monitors': len(active_monitors),
        'total_requests': len(user_requests)
    })

# Add error handlers for production
@app.errorhandler(500)
def handle_500(e):
    logger.error(f"Server error: {str(e)}")
    return render_template('index.html', error="An internal error occurred. Please try again later."), 500

@app.errorhandler(404)
def handle_404(e):
    return redirect(url_for('index'))

# Add this route temporarily to your app.py for debugging
@app.route('/debug')
def debug():
    """Debug route to test Selenium on Railway"""
    try:
        from scraper import scrapeCourses
        courses = scrapeCourses()
        
        if courses:
            sample = dict(list(courses.items())[:3])  # First 3 courses
            return jsonify({
                'status': 'success',
                'total_courses': len(courses),
                'sample_courses': sample,
                'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'Unknown')
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'No courses found',
                'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'Unknown')
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc(),
            'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'Unknown')
        })

if __name__ == '__main__':
    try:
        # Load existing requests and start monitoring
        start_existing_monitors()
        logger.info(f"Starting Open Seat app on port {Config.PORT}")
        
        # Run the app
        app.run(
            host='0.0.0.0', 
            port=Config.PORT, 
            debug=Config.DEBUG, 
            threaded=True
        )
    except Exception as e:
        logger.error(f"Failed to start app: {str(e)}")
        raise

