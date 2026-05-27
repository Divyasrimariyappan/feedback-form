from flask import Flask, request, jsonify, send_from_directory, render_template
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__, static_folder='.', static_url_path='')

VALID_USERNAME = 'admin'
VALID_PASSWORD = 'password123'


# FRONT PAGE
@app.route('/')
def portal():
    return send_from_directory(app.static_folder, 'portal.html')


# LOGIN PAGE
@app.route('/loginpage')
def loginpage():
    return send_from_directory(app.static_folder, 'index.html')


# FEEDBACK FORM PAGE
@app.route('/form')
def form():
    return send_from_directory(app.static_folder, 'form.html')


# LOGIN VALIDATION
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get('username', '')
    password = data.get('password', '')

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return jsonify(success=True)

    return jsonify(
        success=False,
        message='Invalid username or password'
    ), 401


# FEEDBACK SUBMIT
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():

    # Employee Information
    employee_name = request.form.get('employee_name')
    employee_email = request.form.get('employee_email')
    department = request.form.get('department')
    review_period = request.form.get('review_period')

    # Ratings
    quality = request.form.get('quality')
    productivity = request.form.get('productivity')
    communication = request.form.get('communication')
    teamwork = request.form.get('teamwork')
    initiative = request.form.get('initiative')

    # Detailed Feedback
    strengths = request.form.get('strengths')
    improvement = request.form.get('improvement')
    goals = request.form.get('goals')
    comments = request.form.get('comments')
    reviewer = request.form.get('reviewer')

    # Email Subject
    subject = 'Employee Performance Feedback Review'

    # Email Body
    body = f"""
Hello {employee_name},

Your performance feedback review has been completed.

====================================
EMPLOYEE INFORMATION
====================================

Employee Name : {employee_name}

Department : {department}

Review Period : {review_period}


====================================
PERFORMANCE RATINGS
====================================

Quality of Work : {quality}/5

Productivity & Efficiency : {productivity}/5

Communication Skills : {communication}/5

Teamwork & Collaboration : {teamwork}/5

Initiative & Problem Solving : {initiative}/5


====================================
DETAILED FEEDBACK
====================================

Key Strengths:
{strengths}


Areas for Improvement:
{improvement}


Goals for Next Period:
{goals}


====================================
OVERALL ASSESSMENT
====================================

Additional Comments:
{comments}


Reviewer Name:
{reviewer}


Thank You.
HR Department
"""

    # Sender Email
    sender_email = 'divyasrimariyappan3@gmail.com'

    # Gmail App Password
    sender_password = 'nhfa fjvg zium habr'

    # Create Email
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = employee_email

    try:

        # SMTP Connection
        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender_email, sender_password)

        # Send Email
        server.sendmail(
            sender_email,
            employee_email,
            msg.as_string()
        )

        server.quit()

        # Open Success Page
        return send_from_directory(
            app.static_folder,
            'submit1.html'
        )

    except Exception as e:

        return f"Error: {e}"


if __name__ == '__main__':
    app.run(debug=True)